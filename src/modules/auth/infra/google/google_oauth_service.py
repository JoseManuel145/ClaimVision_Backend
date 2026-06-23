from typing import Mapping, Any
import requests
from urllib.parse import urlencode
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from src.core.config import settings
from src.modules.auth.domain.ports import GoogleOAuthPort


class GoogleOAuthService(GoogleOAuthPort):

    def build_auth_url(self) -> str:
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent",
        }
        return "https://accounts.google.com/o/oauth2/auth?" + urlencode(params)

    def exchange_code(self, code: str) -> Mapping[str, Any]:
        url = "https://oauth2.googleapis.com/token"

        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        response = requests.post(url, data=data)
        response.raise_for_status()

        return response.json()

    def verify_id_token(self, token: str) -> Mapping[str, Any]:
        return id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )