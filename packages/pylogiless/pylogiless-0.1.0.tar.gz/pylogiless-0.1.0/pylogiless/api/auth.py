"""
認証関連の機能を提供するモジュール
"""
import time
from typing import Dict, Optional, Tuple

import requests
from requests.exceptions import RequestException


class LogilessAuth:
    """
    LOGILESS APIの認証を処理するクラス
    OAuth2の認可コードフローを実装しています。
    """

    AUTH_URL = "https://app2.logiless.com/oauth/v2/auth"
    TOKEN_URL = "https://app2.logiless.com/oauth2/token"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
    ):
        """
        LogilessAuthクラスの初期化

        Args:
            client_id (str): OAuth2のクライアントID
            client_secret (str): OAuth2のクライアントシークレット
            redirect_uri (str): 認証後のリダイレクトURI
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expires_at: Optional[float] = None

    def get_authorization_url(self) -> str:
        """
        認証URLを生成する

        Returns:
            str: 認証のためのURL
        """
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
        }
        auth_url = f"{self.AUTH_URL}?client_id={params['client_id']}&response_type={params['response_type']}&redirect_uri={params['redirect_uri']}"
        return auth_url

    def fetch_token(self, code: str) -> Dict[str, str]:
        """
        認可コードを使用してアクセストークンとリフレッシュトークンを取得する

        Args:
            code (str): 認証フローから取得した認可コード

        Returns:
            Dict[str, str]: トークン情報を含む辞書

        Raises:
            ValueError: APIからエラーレスポンスが返された場合
            RequestException: リクエスト中にエラーが発生した場合
        """
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }

        response = None
        try:
            response = requests.get(self.TOKEN_URL, params=params)
            response.raise_for_status()
            token_data = response.json()

            self.access_token = token_data.get("access_token")
            self.refresh_token = token_data.get("refresh_token")
            expires_in = token_data.get("expires_in", 0)
            self.token_expires_at = time.time() + int(expires_in)

            return token_data
        except RequestException as e:
            # HTTPエラーを適切に処理してValueErrorに変換
            if response is not None:
                try:
                    error_data = response.json()
                    error_msg = f"APIエラー: {error_data.get('error', 'Unknown')}: {error_data.get('error_description', 'No description')}"
                except (ValueError, KeyError):
                    error_msg = f"APIエラー: {response.text}"
                raise ValueError(error_msg) from e
            raise ValueError(f"API接続エラー: {str(e)}") from e
        except Exception as e:
            # その他の例外
            error_msg = f"エラー: {str(e)}"
            raise ValueError(error_msg) from e

    def refresh_access_token(self) -> Dict[str, str]:
        """
        リフレッシュトークンを使用して新しいアクセストークンを取得する

        Returns:
            Dict[str, str]: 新しいトークン情報を含む辞書

        Raises:
            ValueError: リフレッシュトークンが設定されていない、またはAPIエラーが発生した場合
            RequestException: リクエスト中にエラーが発生した場合
        """
        if not self.refresh_token:
            raise ValueError("リフレッシュトークンが設定されていません")

        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
        }

        response = None
        try:
            response = requests.get(self.TOKEN_URL, params=params)
            response.raise_for_status()
            token_data = response.json()

            self.access_token = token_data.get("access_token")
            self.refresh_token = token_data.get("refresh_token", self.refresh_token)
            expires_in = token_data.get("expires_in", 0)
            self.token_expires_at = time.time() + int(expires_in)

            return token_data
        except RequestException as e:
            # HTTPエラーを適切に処理してValueErrorに変換
            if response is not None:
                try:
                    error_data = response.json()
                    error_msg = f"APIエラー: {error_data.get('error', 'Unknown')}: {error_data.get('error_description', 'No description')}"
                except (ValueError, KeyError):
                    error_msg = f"APIエラー: {response.text}"
                raise ValueError(error_msg) from e
            raise ValueError(f"API接続エラー: {str(e)}") from e
        except Exception as e:
            # その他の例外
            error_msg = f"エラー: {str(e)}"
            raise ValueError(error_msg) from e

    def set_token(self, access_token: str, refresh_token: str, expires_in: int = 2592000) -> None:
        """
        既存のアクセストークンとリフレッシュトークンを設定する

        Args:
            access_token (str): アクセストークン
            refresh_token (str): リフレッシュトークン
            expires_in (int, optional): トークンの有効期限（秒）。デフォルトは30日（2592000秒）
        """
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expires_at = time.time() + int(expires_in)

    def get_auth_header(self) -> Dict[str, str]:
        """
        APIリクエスト用の認証ヘッダーを取得する

        Returns:
            Dict[str, str]: Authorization ヘッダーを含む辞書
        """
        return {"Authorization": f"Bearer {self.access_token}"}

    def is_token_expired(self) -> bool:
        """
        アクセストークンが期限切れかどうかを確認する

        Returns:
            bool: トークンが期限切れの場合はTrue、そうでない場合はFalse
        """
        if not self.token_expires_at or not self.access_token:
            return True
        # 5分の余裕を持たせる
        return time.time() > (self.token_expires_at - 300)

    def ensure_active_token(self) -> Tuple[bool, Optional[str]]:
        """
        アクセストークンが有効であることを確認し、必要に応じてトークンを更新する

        Returns:
            Tuple[bool, Optional[str]]: 
                - トークンが有効であればTrue、そうでなければFalse
                - エラーメッセージ（エラーがない場合はNone）
        """
        if not self.access_token:
            return False, "アクセストークンが設定されていません"

        if self.is_token_expired():
            if not self.refresh_token:
                return False, "トークンの有効期限が切れており、リフレッシュトークンが設定されていません"
            try:
                self.refresh_access_token()
                return True, None
            except Exception as e:
                return False, f"トークンの更新に失敗しました: {str(e)}"

        return True, None
