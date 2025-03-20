# LOGILESS API 認証ガイド

LOGILESS APIは、OAuth 2.0認証フローを使用してアクセスを管理しています。このドキュメントでは、`pylogiless`ライブラリを使用した認証プロセスについて詳しく説明します。

## 目次

- [認証の概要](#認証の概要)
- [認証フロー](#認証フロー)
  - [Step 1: クライアントの初期化](#step-1-クライアントの初期化)
  - [Step 2: 認証URLの取得](#step-2-認証urlの取得)
  - [Step 3: 認可コードの取得](#step-3-認可コードの取得)
  - [Step 4: アクセストークンの取得](#step-4-アクセストークンの取得)
  - [Step 5: トークンの保存](#step-5-トークンの保存)
- [トークンの再利用](#トークンの再利用)
- [トークンの自動更新](#トークンの自動更新)
- [認証エラーの処理](#認証エラーの処理)
- [実装例](#実装例)
  - [Webアプリケーションでの実装](#webアプリケーションでの実装)
  - [CLIアプリケーションでの実装](#cliアプリケーションでの実装)

## 認証の概要

LOGILESS APIは、OAuth 2.0の認可コードフローを使用して認証を行います。このフローには以下のステップが含まれます：

1. ユーザーを認証サーバーにリダイレクトする
2. ユーザーがLOGILESSにログインし、アプリケーションのアクセス権を承認する
3. 認可コードをリダイレクトURIで受け取る
4. 認可コードを使用してアクセストークンとリフレッシュトークンを取得する
5. APIリクエストにアクセストークンを含める

## 認証フロー

### Step 1: クライアントの初期化

まず、`LogilessClient`インスタンスを作成し、必要な認証情報を渡します：

```python
from pylogiless import LogilessClient

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)
```

**必要なパラメータ：**

- `client_id`: LOGILESS管理画面で取得したクライアントID
- `client_secret`: LOGILESS管理画面で取得したクライアントシークレット
- `redirect_uri`: 認可後にリダイレクトされるURI。LOGILESS管理画面で設定したURIと一致している必要があります。

### Step 2: 認証URLの取得

次に、ユーザーを認証サーバーにリダイレクトするためのURLを取得します：

```python
auth_url = client.get_authorization_url()
print(f"次のURLにアクセスして認証してください: {auth_url}")
```

このURLをユーザーに提示し、ブラウザでアクセスするよう促します。

### Step 3: 認可コードの取得

ユーザーが認証と承認を完了すると、認証サーバーが`redirect_uri`にリダイレクトし、URLに`code`パラメータが含まれます：

```
https://your-redirect-uri.com/callback?code=AUTHORIZATION_CODE
```

この`code`パラメータの値を取得して次のステップで使用します。

### Step 4: アクセストークンの取得

認可コードを使用してアクセストークンとリフレッシュトークンを取得します：

```python
try:
    token_info = client.fetch_token(code)
    print(f"アクセストークン: {token_info['access_token']}")
    print(f"リフレッシュトークン: {token_info['refresh_token']}")
    print(f"有効期限: {token_info['expires_in']}秒")
except Exception as e:
    print(f"トークンの取得に失敗しました: {e}")
```

**token_infoに含まれる情報：**

- `access_token`: APIリクエストに使用するアクセストークン
- `refresh_token`: アクセストークンの更新に使用するリフレッシュトークン
- `expires_in`: アクセストークンの有効期限（秒）
- `token_type`: トークンのタイプ（通常は「bearer」）

### Step 5: トークンの保存

取得したトークンを安全に保存し、次回の接続時に再利用できるようにします。トークンはセキュアな方法で保存する必要があります。

```python
# トークン情報を保存する例（実際のアプリケーションでは安全な方法で保存する）
import json

with open('tokens.json', 'w') as f:
    json.dump({
        'access_token': token_info['access_token'],
        'refresh_token': token_info['refresh_token'],
        'expires_at': time.time() + token_info['expires_in']
    }, f)
```

## トークンの再利用

保存したトークンを再利用する場合は、`set_token`メソッドを使用します：

```python
# 保存したトークン情報を読み込む
import json

with open('tokens.json', 'r') as f:
    tokens = json.load(f)

client.set_token(
    access_token=tokens['access_token'],
    refresh_token=tokens['refresh_token'],
    expires_in=int(tokens['expires_at'] - time.time())  # 残り時間を計算
)
```

## トークンの自動更新

`pylogiless`ライブラリは、アクセストークンが期限切れになった場合に自動的にリフレッシュトークンを使用して新しいアクセストークンを取得します。これは`request`メソッドの内部で行われるため、通常は明示的に処理する必要はありません。

以下のシナリオでトークンの自動更新が行われます：

1. APIリクエストが401エラー（Unauthorized）を返す
2. トークンの有効期限が切れていることをクライアントが検出する

リフレッシュに成功すると、新しいアクセストークンとリフレッシュトークンが自動的に設定されます。

## 認証エラーの処理

認証に関連するエラーは`LogilessAuthError`例外でキャッチできます：

```python
from pylogiless import LogilessAuthError

try:
    articles = client.article.list()
except LogilessAuthError as e:
    print(f"認証エラー: {e}")
    # 必要に応じてトークンを再取得するなどの処理
```

主な認証エラーには以下のようなものがあります：

- `invalid_client`: クライアントIDまたはクライアントシークレットが無効
- `invalid_grant`: 認可コードまたはリフレッシュトークンが無効
- `invalid_token`: アクセストークンが無効または期限切れ
- `unauthorized_client`: クライアントに要求されたリソースへのアクセス権がない

## 実装例

### Webアプリケーションでの実装

Flaskを使用した実装例：

```python
from flask import Flask, request, redirect, session
from pylogiless import LogilessClient, LogilessAuthError

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# 環境変数から認証情報を取得
CLIENT_ID = os.environ.get("LOGILESS_CLIENT_ID")
CLIENT_SECRET = os.environ.get("LOGILESS_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/callback"

@app.route('/')
def index():
    return '<a href="/login">LOGILESSでログイン</a>'

@app.route('/login')
def login():
    client = LogilessClient(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    auth_url = client.get_authorization_url()
    session['client_id'] = CLIENT_ID
    session['client_secret'] = CLIENT_SECRET
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "認可コードがありません。", 400
    
    client = LogilessClient(
        session['client_id'],
        session['client_secret'],
        REDIRECT_URI
    )
    
    try:
        token_info = client.fetch_token(code)
        # トークンをセッションに保存
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        return redirect('/dashboard')
    except Exception as e:
        return f"トークンの取得に失敗しました: {e}", 400

@app.route('/dashboard')
def dashboard():
    if 'access_token' not in session:
        return redirect('/login')
    
    client = LogilessClient(
        session['client_id'],
        session['client_secret'],
        REDIRECT_URI
    )
    client.set_token(session['access_token'], session['refresh_token'])
    
    try:
        # APIリクエストの例
        warehouses = client.warehouse.list()
        return f"倉庫数: {len(warehouses.get('items', []))}"
    except LogilessAuthError:
        # 認証エラーの場合、ログインページにリダイレクト
        return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
```

### CLIアプリケーションでの実装

コマンドラインインターフェースでの実装例：

```python
#!/usr/bin/env python
import os
import sys
import json
import time
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import threading

from pylogiless import LogilessClient

# 環境変数から認証情報を取得
CLIENT_ID = os.environ.get("LOGILESS_CLIENT_ID")
CLIENT_SECRET = os.environ.get("LOGILESS_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"
TOKENS_FILE = "logiless_tokens.json"

# コールバック用のHTTPサーバー
class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # URLからコードを取得
        query = parse_qs(urlparse(self.path).query)
        if 'code' in query:
            code = query['code'][0]
            self.server.authorization_code = code
            response = "<html><body><h1>認証成功</h1><p>ブラウザを閉じて、アプリケーションに戻ってください。</p></body></html>"
        else:
            response = "<html><body><h1>認証エラー</h1><p>認可コードが見つかりませんでした。</p></body></html>"
        
        self.wfile.write(response.encode('utf-8'))
    
    def log_message(self, format, *args):
        # ログ出力を抑制
        return

def get_saved_tokens():
    """保存されたトークンを読み込む"""
    try:
        with open(TOKENS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_tokens(token_info):
    """トークンを保存する"""
    with open(TOKENS_FILE, 'w') as f:
        json.dump({
            'access_token': token_info['access_token'],
            'refresh_token': token_info['refresh_token'],
            'expires_at': time.time() + token_info['expires_in']
        }, f)

def authenticate():
    """認証フローを実行する"""
    client = LogilessClient(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    
    # 保存されたトークンがあれば使用
    tokens = get_saved_tokens()
    if tokens and time.time() < tokens['expires_at']:
        print("保存されたトークンを使用します。")
        client.set_token(tokens['access_token'], tokens['refresh_token'])
        return client
    
    # 新規認証が必要
    auth_url = client.get_authorization_url()
    print(f"ブラウザを開いて認証を行います: {auth_url}")
    
    # ブラウザを開く
    webbrowser.open(auth_url)
    
    # コールバックを待機
    server = HTTPServer(('localhost', 8000), CallbackHandler)
    server.authorization_code = None
    
    # 別スレッドでサーバーを起動
    server_thread = threading.Thread(target=server.handle_request)
    server_thread.start()
    
    print("ブラウザで認証を完了するまで待機中...")
    server_thread.join()
    
    if not server.authorization_code:
        print("認証に失敗しました。認可コードが取得できませんでした。")
        sys.exit(1)
    
    # トークンを取得
    try:
        token_info = client.fetch_token(server.authorization_code)
        print("認証に成功しました。")
        
        # トークンを保存
        save_tokens(token_info)
        
        return client
    except Exception as e:
        print(f"トークンの取得に失敗しました: {e}")
        sys.exit(1)

def main():
    """メイン処理"""
    if not (CLIENT_ID and CLIENT_SECRET):
        print("エラー: 環境変数 LOGILESS_CLIENT_ID と LOGILESS_CLIENT_SECRET を設定してください。")
        sys.exit(1)
    
    try:
        # 認証を実行
        client = authenticate()
        
        # APIリクエストの例
        print("\n倉庫情報を取得中...")
        warehouses = client.warehouse.list()
        print(f"倉庫数: {len(warehouses.get('items', []))}")
        
        print("\n在庫情報を取得中...")
        inventory = client.actual_inventory_summary.list(limit=5)
        print(f"在庫アイテム数: {inventory.get('total', 0)}")
        
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

このドキュメントでは、LOGILESS API認証フローの詳細と実装例を提供しています。環境や要件に合わせてコードを調整してください。 