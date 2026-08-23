import logging
import os
from urllib.parse import urlencode

from django.shortcuts import redirect
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as SimpleJWTTokenRefreshView

from .authentication import CustomJWTAuthentication
from .services import GoogleOAuthProvider, OAuthUserService

logger = logging.getLogger(__name__)


def set_auth_cookies(response, access_token: str, refresh_token: str = None):
    """Helper utility to set both access and refresh cookies consistently."""
    is_debug = os.getenv('DEBUG', 'False') == 'True'
    cookie_domain = os.getenv('COOKIE_DOMAIN', None)

    response.set_cookie(
        key='at',
        value=access_token,
        httponly=False,
        secure=not is_debug,
        samesite='Lax',
        domain=cookie_domain,
        max_age=5 * 60,
    )

    if refresh_token:
        response.set_cookie(
            key='rt',
            value=refresh_token,
            httponly=True,
            secure=not is_debug,
            samesite='Lax',
            domain=cookie_domain,
            max_age=12 * 3600,
        )


class CookieTokenRefreshView(SimpleJWTTokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('rt')

        if not refresh_token:
            return Response(
                {'error': 'Refresh token missing from cookies'}, status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except (TokenError, InvalidToken) as e:
            return Response({'error': e.args[0]}, status=status.HTTP_401_UNAUTHORIZED)

        data = serializer.validated_data
        response = Response({'access': data['access']}, status=status.HTTP_200_OK)

        new_refresh = data.get('refresh', refresh_token)
        set_auth_cookies(response, access_token=data['access'], refresh_token=new_refresh)

        return response


class ProtectedProfileView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            {
                'id': request.user.id,
                'email': request.user.login_email,
                'username': request.user.username,
            }
        )


class LogoutView(APIView):
    """Blacklists the refresh token and clears all HTTP cookies."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('rt')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except (TokenError, InvalidToken):
                pass

        response = Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        response.delete_cookie('rt')
        response.delete_cookie('at')
        return response


class GoogleOAuthUrlView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        client_id = os.getenv('GOOGLE_CLIENT_ID')
        redirect_uri = 'http://localhost:8000/api/auth/callback'

        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'access_type': 'offline',
            'prompt': 'consent',
        }

        url = f'https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}'
        return Response({'url': url}, status=status.HTTP_200_OK)


class GoogleCallbackView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
        redirect_url = os.getenv('FRONTEND_REDIRECT_URL', f'{frontend_url}/dashboard')
        code = request.query_params.get('code')

        redirect_uri = 'http://localhost:8000/api/auth/callback'

        if not code:
            return redirect(f'{frontend_url}/login?error=no_code')

        try:
            provider = GoogleOAuthProvider()
            service = OAuthUserService(provider=provider)
            user = service.authenticate_or_create_user(code=code, redirect_uri=redirect_uri)
            tokens = service.generate_jwt_tokens(user)

            response = redirect(redirect_url)

            set_auth_cookies(
                response, access_token=tokens['access'], refresh_token=tokens['refresh']
            )

            return response
        except ValueError as exc:
            logger.warning(f'OAuth validation failed: {exc}')
            return redirect(f'{frontend_url}/login?error=invalid_credentials')
        except Exception:
            logger.exception('Unexpected error during OAuth login')
            return redirect(f'{frontend_url}/login?error=auth_failed')
