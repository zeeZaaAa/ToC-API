import os
from abc import ABC, abstractmethod
from typing import Any

import requests
from rest_framework_simplejwt.tokens import RefreshToken

from src.users.services import UserService


class BaseOAuthProvider(ABC):
    @abstractmethod
    def verify_code_and_get_user_info(self, code: str, redirect_uri: str | None = None) -> dict[str, Any]:
        """Exchange authorization code with provider using backend credentials and return user info dict."""


class GoogleOAuthProvider(BaseOAuthProvider):
    TOKEN_URL = 'https://oauth2.googleapis.com/token'
    USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'

    def __init__(self):
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.default_redirect_uri = os.getenv('FRONTEND_REDIRECT_URL', 'http://localhost:5173')

    def verify_code_and_get_user_info(self, code: str, redirect_uri: str | None = None) -> dict[str, Any]:
        target_redirect_uri = redirect_uri or self.default_redirect_uri

        token_payload = {
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': target_redirect_uri,
            'grant_type': 'authorization_code',
        }

        token_response = requests.post(self.TOKEN_URL, data=token_payload, timeout=5)
        if token_response.status_code != 200:
            raise ValueError('Failed to exchange authorization code with Google')

        access_token = token_response.json().get('access_token')
        if not access_token:
            raise ValueError('Access token not present in Google token response')

        user_info_response = requests.get(
            self.USER_INFO_URL,
            headers={'Authorization': f'Bearer {access_token}'},
            timeout=5,
        )
        if user_info_response.status_code != 200:
            raise ValueError('Failed to fetch user info from Google')

        data = user_info_response.json()
        return {
            'oauth_id': data.get('sub'),
            'email': data.get('email'),
            'username': data.get('name', ''),
        }


class OAuthUserService:
    def __init__(self, provider: BaseOAuthProvider, user_service: UserService | None = None):
        self.provider = provider
        self.user_service = user_service if user_service is not None else UserService()

    def authenticate_or_create_user(self, code: str, redirect_uri: str | None = None) -> Any:
        """Verifies OAuth code and delegates user creation to UserService."""
        user_data = self.provider.verify_code_and_get_user_info(code=code, redirect_uri=redirect_uri)
        return self.user_service.get_or_create_oauth_user(user_data)

    @staticmethod
    def generate_jwt_tokens(user: Any) -> dict[str, str]:
        """Generates JWT access and refresh tokens for a given user entity."""
        refresh = RefreshToken.for_user(user)
        return {'access': str(refresh.access_token), 'refresh': str(refresh)}