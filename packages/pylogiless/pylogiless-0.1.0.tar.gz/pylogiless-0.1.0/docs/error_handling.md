# LOGILESS API エラーハンドリングガイド

このドキュメントでは、`pylogiless`ライブラリを使用する際のエラーハンドリング方法について説明します。

## 目次

- [エラーの種類](#エラーの種類)
- [例外クラス階層](#例外クラス階層)
- [基本的なエラーハンドリング](#基本的なエラーハンドリング)
- [特定のエラータイプの処理](#特定のエラータイプの処理)
- [エラーの詳細情報へのアクセス](#エラーの詳細情報へのアクセス)
- [リトライ戦略](#リトライ戦略)
- [パターン別エラーハンドリング例](#パターン別エラーハンドリング例)

## エラーの種類

LOGILESS APIとの通信中に発生する可能性のあるエラーは、大きく以下のカテゴリに分類されます：

### クライアント側のエラー (4xx)

- **認証エラー (401)**: トークンが無効や期限切れの場合に発生
- **権限エラー (403)**: リソースへのアクセス権限がない場合に発生
- **リソース不存在エラー (404)**: 要求されたリソースが見つからない場合に発生
- **バリデーションエラー (400)**: リクエストパラメータが無効な場合に発生
- **レート制限エラー (429)**: 短時間に多すぎるリクエストを行った場合に発生
- **リソースロックエラー (423)**: リソースが他のプロセスによってロックされている場合に発生

### サーバー側のエラー (5xx)

- **サーバーエラー (500)**: サーバー内部でエラーが発生した場合
- **サービス利用不可エラー (503)**: サービスが一時的に利用できない場合

## 例外クラス階層

`pylogiless`ライブラリでは、以下の例外クラス階層を使用してエラーを表現します：

- `LogilessError` - 基本例外クラス
  - `LogilessAuthError` - 認証関連のエラー (401)
  - `LogilessPermissionError` - 権限関連のエラー (403)
  - `LogilessResourceNotFoundError` - リソースが見つからないエラー (404)
  - `LogilessValidationError` - バリデーションエラー (400)
  - `LogilessRateLimitError` - レート制限エラー (429)
  - `LogilessResourceLockedError` - リソースロックエラー (423)
  - `LogilessServerError` - サーバー側のエラー (5xx)

## 基本的なエラーハンドリング

最も基本的なエラーハンドリングは、`LogilessError`をキャッチすることです。これにより、すべてのAPI関連のエラーを捕捉できます：

```python
from pylogiless import LogilessClient, LogilessError

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)

try:
    # APIリクエストを実行
    articles = client.article.list()
    print(f"商品数: {articles.get('total', 0)}")
except LogilessError as e:
    print(f"APIエラーが発生しました: {e}")
```

## 特定のエラータイプの処理

特定のエラータイプに対して異なる処理を行いたい場合は、個別の例外クラスをキャッチします：

```python
from pylogiless import (
    LogilessClient,
    LogilessError,
    LogilessAuthError,
    LogilessResourceNotFoundError,
    LogilessValidationError,
    LogilessRateLimitError,
    LogilessServerError
)

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)

try:
    # APIリクエストを実行
    article = client.article.get("ARTICLE_ID")
except LogilessAuthError as e:
    print(f"認証エラー: {e}")
    # トークンの再取得などの処理
except LogilessResourceNotFoundError as e:
    print(f"リソースが見つかりません: {e}")
    # 存在しないリソースに対する処理
except LogilessValidationError as e:
    print(f"バリデーションエラー: {e}")
    # パラメータの修正など
except LogilessRateLimitError as e:
    print(f"レート制限エラー: {e}")
    # 一定時間待機する処理
except LogilessServerError as e:
    print(f"サーバーエラー: {e}")
    # サーバー側のエラーを記録して後で再試行
except LogilessError as e:
    print(f"その他のAPIエラー: {e}")
```

## エラーの詳細情報へのアクセス

例外オブジェクトから、エラーに関する詳細情報を取得できます：

```python
try:
    client.article.create({"invalid_data": "value"})
except LogilessValidationError as e:
    print(f"エラーコード: {e.code}")
    print(f"エラーメッセージ: {e.message}")
    
    # バリデーションエラーの詳細フィールド（エラーがフィールド単位で返される場合）
    if hasattr(e, 'errors') and e.errors:
        for field, error in e.errors.items():
            print(f"フィールド '{field}': {error}")
```

APIからのレスポンス全体を確認したい場合：

```python
try:
    client.article.update("ARTICLE_ID", {"status": "INVALID_STATUS"})
except LogilessError as e:
    # 生のレスポンスデータにアクセス（存在する場合）
    if hasattr(e, 'response') and e.response:
        print(f"ステータスコード: {e.response.status_code}")
        print(f"レスポンスヘッダー: {e.response.headers}")
        print(f"レスポンス本文: {e.response.text}")
```

## リトライ戦略

一時的なエラー（ネットワークエラーやサーバーエラー）に対しては、リトライ戦略を実装することをお勧めします：

```python
import time
from requests.exceptions import RequestException
from pylogiless import LogilessClient, LogilessServerError, LogilessRateLimitError

def retry_with_backoff(func, max_retries=3, base_delay=1):
    """
    エクスポネンシャルバックオフを使用して関数を再試行する
    
    Args:
        func: 再試行する関数
        max_retries: 最大再試行回数
        base_delay: 基本遅延時間（秒）
    
    Returns:
        関数の戻り値
    """
    retries = 0
    while True:
        try:
            return func()
        except (RequestException, LogilessServerError, LogilessRateLimitError) as e:
            retries += 1
            if retries > max_retries:
                raise e
            
            # エクスポネンシャルバックオフ + ジッタ
            delay = base_delay * (2 ** (retries - 1)) + (random.random() * 0.5)
            print(f"エラー: {e}. {delay:.2f}秒後に再試行します ({retries}/{max_retries})...")
            time.sleep(delay)

# 使用例
client = LogilessClient(client_id="...", client_secret="...", redirect_uri="...")

try:
    # リトライ戦略を適用してAPIを呼び出す
    articles = retry_with_backoff(lambda: client.article.list())
    print(f"商品数: {articles.get('total', 0)}")
except Exception as e:
    print(f"最大再試行回数を超えました: {e}")
```

## パターン別エラーハンドリング例

### 例1: アクセストークンが期限切れの場合の自動更新

`pylogiless`はアクセストークンの期限切れを自動的に処理しますが、手動で処理する場合の例：

```python
from pylogiless import LogilessClient, LogilessAuthError

client = LogilessClient(client_id="...", client_secret="...", redirect_uri="...")
client.set_token("EXPIRED_ACCESS_TOKEN", "REFRESH_TOKEN")

try:
    articles = client.article.list()
except LogilessAuthError as e:
    if "token expired" in str(e).lower():
        print("トークンの有効期限が切れました。更新します...")
        token_info = client.auth.refresh_access_token()
        print(f"トークンを更新しました。新しい有効期限: {token_info['expires_in']}秒")
        
        # 更新されたトークンで再試行
        articles = client.article.list()
    else:
        # その他の認証エラー
        print(f"認証エラー: {e}")
```

### 例2: バリデーションエラーの詳細処理

```python
from pylogiless import LogilessClient, LogilessValidationError

client = LogilessClient(client_id="...", client_secret="...", redirect_uri="...")

# 商品データ（バリデーションに失敗する可能性がある）
article_data = {
    "article_code": "",  # 空の商品コード（必須項目）
    "minimum_lot_size": -1,  # 負の値（不正な値）
}

try:
    new_article = client.article.create(article_data)
except LogilessValidationError as e:
    print(f"バリデーションエラー: {e.message}")
    
    if hasattr(e, 'errors') and e.errors:
        # 各フィールドのエラーを処理
        corrected_data = article_data.copy()
        
        for field, error in e.errors.items():
            print(f"フィールド '{field}': {error}")
            
            # フィールド固有の修正処理
            if field == "article_code" and "required" in str(error).lower():
                corrected_data["article_code"] = "DEFAULT_CODE"
            elif field == "minimum_lot_size" and "positive" in str(error).lower():
                corrected_data["minimum_lot_size"] = 1
        
        print("\n修正されたデータ:")
        for key, value in corrected_data.items():
            if key in e.errors:
                print(f"{key}: {value} (修正済み)")
            else:
                print(f"{key}: {value}")
```

### 例3: レート制限の処理

```python
from pylogiless import LogilessClient, LogilessRateLimitError
import time

client = LogilessClient(client_id="...", client_secret="...", redirect_uri="...")

# 多くのAPIリクエストを処理
items = []
offset = 0
limit = 100
total = None

while total is None or offset < total:
    try:
        response = client.article.list(offset=offset, limit=limit)
        items.extend(response.get("items", []))
        
        if total is None:
            total = response.get("total", 0)
        
        offset += limit
        print(f"進捗: {min(offset, total)}/{total} アイテム取得済み")
        
    except LogilessRateLimitError as e:
        # レート制限エラーの処理
        retry_after = 60  # デフォルトの待機時間（秒）
        
        # レスポンスヘッダーからRetry-Afterを取得（存在する場合）
        if hasattr(e, 'response') and e.response and 'Retry-After' in e.response.headers:
            retry_after = int(e.response.headers['Retry-After'])
        
        print(f"レート制限に達しました。{retry_after}秒後に再試行します...")
        time.sleep(retry_after)
```

正しいエラーハンドリングは、堅牢なアプリケーションを構築するための重要な要素です。`pylogiless`ライブラリの例外クラスを活用して、アプリケーションにおける様々なエラーシナリオに適切に対処しましょう。 