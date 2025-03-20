# pylogiless API リファレンス

このドキュメントでは、`pylogiless`ライブラリを使用してLOGILESS APIの各エンドポイントにアクセスする方法について説明します。

## 目次

- [認証と初期化](#認証と初期化)
- [API共通仕様](#api共通仕様)
- [商品(Article)](#商品article)
- [実在庫サマリ(ActualInventorySummary)](#実在庫サマリactualinventorysummary)
- [論理在庫サマリ(LogicalInventorySummary)](#論理在庫サマリlogicalinventorysummary)
- [出荷配送(OutboundDelivery)](#出荷配送outbounddelivery)
- [入荷配送(InboundDelivery)](#入荷配送inbounddelivery)
- [受注(SalesOrder)](#受注salesorder)
- [倉庫(Warehouse)](#倉庫warehouse)
- [店舗(Store)](#店舗store)
- [ロケーション(Location)](#ロケーションlocation)
- [エラーハンドリング](#エラーハンドリング)

## 認証と初期化

LOGILESS APIはOAuth2認証を使用しています。`pylogiless`ライブラリを使用するには、以下の手順で認証を行います。

### クライアントの初期化

```python
from pylogiless import LogilessClient

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)
```

### 認証URLの取得と認可コードの取得

```python
# 認証URLを取得
auth_url = client.get_authorization_url()
print(f"次のURLにアクセスして認証してください: {auth_url}")

# ユーザーが認証後、リダイレクトURLからcodeパラメータを取得
# これは通常、Webアプリケーションでコールバックとして実装します
code = "AUTHORIZATION_CODE"  # リダイレクトURLから取得した認可コード
```

### アクセストークンの取得

```python
# 認可コードを使用してトークンを取得
token_info = client.fetch_token(code)
print(f"アクセストークン: {token_info['access_token']}")
print(f"リフレッシュトークン: {token_info['refresh_token']}")
print(f"有効期限: {token_info['expires_in']}秒")
```

### 既存のトークンを使用

アクセストークンとリフレッシュトークンを既に持っている場合は、以下のように設定します。

```python
client.set_token(
    access_token="ACCESS_TOKEN",
    refresh_token="REFRESH_TOKEN",
    expires_in=2592000  # オプション、デフォルトは30日
)
```

## API共通仕様

LOGILESS APIの各エンドポイントは、以下の共通のメソッドをサポートしています。

### 共通パラメータ

リストメソッド(`list()`)で使用できる共通のクエリパラメータ：

- `limit`: 取得する最大件数
- `offset`: 取得開始位置（ページネーション用）
- `sort`: ソート条件
- `filter`: フィルター条件

### 共通メソッド

各リソースには以下の共通メソッドがあります：

- `get(resource_id, **params)`: 特定のリソースを取得
- `list(**params)`: リソースのリストを取得
- `create(data)`: 新しいリソースを作成
- `update(resource_id, data)`: 既存のリソースを更新
- `delete(resource_id)`: リソースを削除

## 商品(Article)

商品情報を管理するAPIです。

### 商品リストの取得

```python
# すべての商品を取得
articles = client.article.list()

# 最大10件の商品を取得
articles = client.article.list(limit=10)

# 商品コードで検索
articles = client.article.list(filter={"article_code": "SAMPLE001"})
```

### 特定の商品の取得

```python
# 商品IDを指定して取得
article = client.article.get("ARTICLE_ID")
```

### 商品の作成

```python
# 新しい商品を作成
new_article = client.article.create({
    "article_code": "SAMPLE001",
    "article_name": "サンプル商品",
    "article_name_kana": "サンプルショウヒン",
    "unit_of_measure": "個",
    "minimum_lot_size": 1
})
```

### 商品の更新

```python
# 商品情報を更新
updated_article = client.article.update("ARTICLE_ID", {
    "article_name": "更新後の商品名",
    "article_name_kana": "コウシンゴノショウヒンメイ"
})
```

### 商品の削除

```python
# 商品を削除
result = client.article.delete("ARTICLE_ID")
```

## 実在庫サマリ(ActualInventorySummary)

実際の在庫数を管理するAPIです。

### 在庫リストの取得

```python
# すべての在庫情報を取得
inventory = client.actual_inventory_summary.list()

# 特定の倉庫の在庫情報を取得
inventory = client.actual_inventory_summary.list(
    filter={"warehouse_id": "WAREHOUSE_ID"}
)

# 特定の商品の在庫情報を取得
inventory = client.actual_inventory_summary.list(
    filter={"article_id": "ARTICLE_ID"}
)
```

### 特定の在庫情報の取得

```python
# 在庫IDを指定して取得
inventory_item = client.actual_inventory_summary.get("INVENTORY_ID")
```

## 論理在庫サマリ(LogicalInventorySummary)

予約や引当を含めた論理的な在庫数を管理するAPIです。

### 論理在庫リストの取得

```python
# すべての論理在庫情報を取得
logical_inventory = client.logical_inventory_summary.list()

# 特定の倉庫の論理在庫情報を取得
logical_inventory = client.logical_inventory_summary.list(
    filter={"warehouse_id": "WAREHOUSE_ID"}
)

# 特定の商品の論理在庫情報を取得
logical_inventory = client.logical_inventory_summary.list(
    filter={"article_id": "ARTICLE_ID"}
)
```

### 特定の論理在庫情報の取得

```python
# 論理在庫IDを指定して取得
logical_inventory_item = client.logical_inventory_summary.get("LOGICAL_INVENTORY_ID")
```

## 出荷配送(OutboundDelivery)

出荷に関する情報を管理するAPIです。

### 出荷配送リストの取得

```python
# すべての出荷配送情報を取得
outbound_deliveries = client.outbound_delivery.list()

# 特定の倉庫の出荷配送情報を取得
outbound_deliveries = client.outbound_delivery.list(
    filter={"warehouse_id": "WAREHOUSE_ID"}
)

# 特定の配送状態の出荷配送情報を取得
outbound_deliveries = client.outbound_delivery.list(
    filter={"status": "PICKING"}
)
```

### 特定の出荷配送の取得

```python
# 出荷配送IDを指定して取得
outbound_delivery = client.outbound_delivery.get("OUTBOUND_DELIVERY_ID")
```

### 出荷配送の作成

```python
# 新しい出荷配送を作成
new_outbound_delivery = client.outbound_delivery.create({
    "warehouse_id": "WAREHOUSE_ID",
    "store_id": "STORE_ID",
    "scheduled_date": "2023-12-31",
    "items": [
        {
            "article_id": "ARTICLE_ID",
            "quantity": 10
        }
    ]
})
```

### 出荷配送の更新

```python
# 出荷配送情報を更新
updated_outbound_delivery = client.outbound_delivery.update("OUTBOUND_DELIVERY_ID", {
    "scheduled_date": "2024-01-15",
    "items": [
        {
            "article_id": "ARTICLE_ID",
            "quantity": 15
        }
    ]
})
```

## 入荷配送(InboundDelivery)

入荷に関する情報を管理するAPIです。

### 入荷配送リストの取得

```python
# すべての入荷配送情報を取得
inbound_deliveries = client.inbound_delivery.list()

# 特定の倉庫の入荷配送情報を取得
inbound_deliveries = client.inbound_delivery.list(
    filter={"warehouse_id": "WAREHOUSE_ID"}
)

# 特定の配送状態の入荷配送情報を取得
inbound_deliveries = client.inbound_delivery.list(
    filter={"status": "RECEIVED"}
)
```

### 特定の入荷配送の取得

```python
# 入荷配送IDを指定して取得
inbound_delivery = client.inbound_delivery.get("INBOUND_DELIVERY_ID")
```

### 入荷配送の作成

```python
# 新しい入荷配送を作成
new_inbound_delivery = client.inbound_delivery.create({
    "warehouse_id": "WAREHOUSE_ID",
    "supplier_id": "SUPPLIER_ID",
    "scheduled_date": "2023-12-31",
    "items": [
        {
            "article_id": "ARTICLE_ID",
            "quantity": 100
        }
    ]
})
```

### 入荷配送の更新

```python
# 入荷配送情報を更新
updated_inbound_delivery = client.inbound_delivery.update("INBOUND_DELIVERY_ID", {
    "scheduled_date": "2024-01-15",
    "items": [
        {
            "article_id": "ARTICLE_ID",
            "quantity": 150
        }
    ]
})
```

## 受注(SalesOrder)

受注情報を管理するAPIです。

### 受注リストの取得

```python
# すべての受注情報を取得
sales_orders = client.sales_order.list()

# 特定の倉庫の受注情報を取得
sales_orders = client.sales_order.list(
    filter={"warehouse_id": "WAREHOUSE_ID"}
)

# 特定の受注状態の受注情報を取得
sales_orders = client.sales_order.list(
    filter={"status": "NEW"}
)
```

### 特定の受注の取得

```python
# 受注IDを指定して取得
sales_order = client.sales_order.get("SALES_ORDER_ID")
```

### 受注の作成

```python
# 新しい受注を作成
new_sales_order = client.sales_order.create({
    "order_number": "ORDER123",
    "customer_id": "CUSTOMER_ID",
    "order_date": "2023-12-31",
    "warehouse_id": "WAREHOUSE_ID",
    "items": [
        {
            "article_id": "ARTICLE_ID",
            "quantity": 2,
            "unit_price": 1000
        }
    ]
})
```

### 受注の更新

```python
# 受注情報を更新
updated_sales_order = client.sales_order.update("SALES_ORDER_ID", {
    "status": "CONFIRMED",
    "items": [
        {
            "article_id": "ARTICLE_ID",
            "quantity": 3,
            "unit_price": 950
        }
    ]
})
```

## 倉庫(Warehouse)

倉庫情報を管理するAPIです。

### 倉庫リストの取得

```python
# すべての倉庫情報を取得
warehouses = client.warehouse.list()
```

### 特定の倉庫の取得

```python
# 倉庫IDを指定して取得
warehouse = client.warehouse.get("WAREHOUSE_ID")
```

## 店舗(Store)

店舗情報を管理するAPIです。

### 店舗リストの取得

```python
# すべての店舗情報を取得
stores = client.store.list()
```

### 特定の店舗の取得

```python
# 店舗IDを指定して取得
store = client.store.get("STORE_ID")
```

## ロケーション(Location)

倉庫内のロケーション（保管場所）情報を管理するAPIです。

### ロケーションリストの取得

```python
# すべてのロケーション情報を取得
locations = client.location.list()

# 特定の倉庫のロケーション情報を取得
locations = client.location.list(
    filter={"warehouse_id": "WAREHOUSE_ID"}
)
```

### 特定のロケーションの取得

```python
# ロケーションIDを指定して取得
location = client.location.get("LOCATION_ID")
```

## エラーハンドリング

`pylogiless`ライブラリは、APIリクエスト中に発生するエラーを適切に処理するための例外クラスを提供しています。

### 主な例外クラス

- `LogilessError`: 基本的なエラークラス
- `LogilessAuthError`: 認証関連のエラー
- `LogilessValidationError`: バリデーションエラー
- `LogilessRateLimitError`: レート制限に達した場合のエラー
- `LogilessResourceLockedError`: リソースがロックされている場合のエラー
- `LogilessServerError`: サーバー側のエラー

### エラーハンドリングの例

```python
from pylogiless import (
    LogilessError,
    LogilessAuthError,
    LogilessValidationError,
    LogilessRateLimitError
)

try:
    article = client.article.get("NON_EXISTENT_ID")
except LogilessAuthError as e:
    print(f"認証エラー: {e}")
    # トークンの更新などの処理
except LogilessValidationError as e:
    print(f"バリデーションエラー: {e}")
    # 入力値の修正など
except LogilessRateLimitError as e:
    print(f"レート制限エラー: {e}")
    # 一定時間待機するなど
except LogilessError as e:
    print(f"その他のエラー: {e}")
```

詳細なエラー情報へのアクセス:

```python
try:
    article = client.article.create({"invalid_data": "value"})
except LogilessValidationError as e:
    print(f"エラーコード: {e.code}")
    print(f"エラーメッセージ: {e.message}")
    if hasattr(e, 'errors') and e.errors:
        for field, error in e.errors.items():
            print(f"フィールド {field}: {error}")
``` 