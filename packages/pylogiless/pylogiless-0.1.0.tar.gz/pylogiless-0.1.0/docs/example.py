#!/usr/bin/env python
"""
LOGILESS API クライアントライブラリの使用例
"""
import os
import sys
import time

from pylogiless import LogilessClient

# 環境変数から認証情報を取得
CLIENT_ID = os.environ.get("LOGILESS_CLIENT_ID")
CLIENT_SECRET = os.environ.get("LOGILESS_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("LOGILESS_REDIRECT_URI", "http://localhost:8000/callback")
ACCESS_TOKEN = os.environ.get("LOGILESS_ACCESS_TOKEN")
REFRESH_TOKEN = os.environ.get("LOGILESS_REFRESH_TOKEN")


def print_divider(title):
    """
    セクションの区切りを表示する
    """
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")


def print_json(data):
    """
    JSONデータを見やすく表示する
    """
    import json
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    """
    メイン処理
    """
    # 必須情報をチェック
    if not (CLIENT_ID and CLIENT_SECRET):
        print("エラー: 環境変数 LOGILESS_CLIENT_ID と LOGILESS_CLIENT_SECRET を設定してください。")
        sys.exit(1)

    # クライアントインスタンスを作成
    client = LogilessClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
    )

    # 既存のトークンがあれば設定
    if ACCESS_TOKEN and REFRESH_TOKEN:
        print("既存のアクセストークンとリフレッシュトークンを使用します。")
        client.set_token(ACCESS_TOKEN, REFRESH_TOKEN)
    else:
        # 認証URLを取得して表示
        auth_url = client.get_authorization_url()
        print_divider("認証手順")
        print(f"以下のURLにアクセスして認証してください:\n{auth_url}")
        print("\n認証後、リダイレクトURLのcode=以降の値をコピーしてください。")
        
        # 認可コードを入力してもらう
        auth_code = input("\n認可コードを入力してください: ").strip()
        
        try:
            # トークンを取得
            token_info = client.fetch_token(auth_code)
            print("\nトークンの取得に成功しました。")
            print(f"今後の実行のために、以下の環境変数を設定することをお勧めします:\n")
            print(f"export LOGILESS_ACCESS_TOKEN={token_info['access_token']}")
            print(f"export LOGILESS_REFRESH_TOKEN={token_info['refresh_token']}")
        except Exception as e:
            print(f"エラー: トークンの取得に失敗しました: {e}")
            sys.exit(1)

    # APIリクエストの例
    try:
        # 在庫情報を取得
        print_divider("在庫情報の取得")
        inventory = client.actual_inventory_summary.list(limit=5)
        print_json(inventory)

        # 倉庫情報を取得
        print_divider("倉庫情報の取得")
        warehouses = client.warehouse.list()
        print_json(warehouses)

        # 商品情報を取得
        print_divider("商品情報の取得")
        articles = client.article.list(limit=5)
        print_json(articles)
        
        # 新しく追加されたAPIリソースの使用例
        
        # サプライヤー情報を取得
        print_divider("サプライヤー情報の取得")
        suppliers = client.supplier.list(limit=5)
        print_json(suppliers)
        
        # 再注文点の情報を取得
        print_divider("再注文点の情報取得")
        reorder_points = client.reorder_point.list(limit=5)
        print_json(reorder_points)
        
        # 取引ログの取得
        print_divider("取引ログの取得")
        logs = client.transaction_log.list(limit=5)
        print_json(logs)
        
        # 日次在庫サマリの取得
        print_divider("日次在庫サマリの取得")
        daily_inventory = client.daily_inventory_summary.list(limit=5)
        print_json(daily_inventory)
        
        # 商品マッピングの取得
        print_divider("商品マッピングの取得")
        article_maps = client.article_map.list(limit=5)
        print_json(article_maps)
        
        # 倉庫間移動の情報取得
        print_divider("倉庫間移動の情報取得")
        transfers = client.inter_warehouse_transfer.list(limit=5)
        print_json(transfers)

    except Exception as e:
        print(f"エラー: APIリクエスト中にエラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 