import logging
import os
from urllib.parse import urlencode

from django.shortcuts import redirect
from requests.exceptions import RequestException
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as SimpleJWTTokenRefreshView

from .authentication import CustomJWTAuthentication
from .services import GoogleOAuthProvider, OAuthUserService

logger = logging.getLogger(__name__)


def set_refresh_cookie(response: Response, refresh_token: str):
    """Helper utility to set only the HttpOnly refresh token cookie."""
    is_debug = os.getenv('DEBUG', 'False') == 'True'
    cookie_domain = os.getenv('COOKIE_DOMAIN', None)

    response.set_cookie(
        key='rt',
        value=refresh_token,
        httponly=True,
        secure=not is_debug,
        samesite='None' if not is_debug else 'Lax',
        domain=cookie_domain,
        max_age=12 * 3600,
    )


class CookieTokenRefreshView(SimpleJWTTokenRefreshView):
    def post(self, request, *args, **kwargs):
        print('Received Cookies:', request.COOKIES)
        refresh_token = request.COOKIES.get('rt')

        if not refresh_token:
            return Response(
                {'error': 'Refresh token missing from cookies'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except (TokenError, InvalidToken) as e:
            return Response({'error': e.args[0]}, status=status.HTTP_401_UNAUTHORIZED)

        data = serializer.validated_data

        response = Response({'at': data['access']}, status=status.HTTP_200_OK)

        new_refresh = data.get('refresh', refresh_token)
        set_refresh_cookie(response, refresh_token=new_refresh)

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
    """Blacklists the refresh token and clears the refresh cookie."""

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
        return response


class GoogleCallbackView(APIView):
    """Step 4 & 5: Process Google Code, set cookie, and redirect to Frontend"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        code = request.query_params.get('code')
        error_param = request.query_params.get('error')
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
        redirect_url = os.getenv('FRONTEND_REDIRECT_URL', 'http://localhost:5173/')
        backend_redirect_uri = os.getenv(
            'GOOGLE_BACKEND_REDIRECT_URI', 'http://localhost:8000/api/auth/callback/'
        )

        if error_param:
            logger.info(f'Google OAuth cancelled by user: {error_param}')
            return redirect(f'{frontend_url}/login?error=access_denied')

        if not code:
            return redirect(f'{frontend_url}/login?error=no_code')

        try:
            provider = GoogleOAuthProvider()
            service = OAuthUserService(provider=provider)

            user = service.authenticate_or_create_user(code=code, redirect_uri=backend_redirect_uri)
            tokens = service.generate_jwt_tokens(user)

            target_redirect_url = redirect_url
            response = redirect(target_redirect_url)

            set_refresh_cookie(response, refresh_token=tokens['refresh'])

            return response

        except RequestException as exc:
            logger.error(f'Network error communicating with Google OAuth servers: {exc}')
            return redirect(f'{frontend_url}/login?error=provider_unavailable')

        except (ValueError, KeyError) as exc:
            logger.warning(f'OAuth payload or token exchange validation failed: {exc}')
            return redirect(f'{frontend_url}/login?error=invalid_token')

        except TokenError as exc:
            logger.warning(f'Internal JWT token generation failed: {exc}')
            return redirect(f'{frontend_url}/login?error=token_generation_failed')


class GoogleLoginRedirectView(APIView):
    """Step 1 & 2: Redirect user directly to Google Consent Page"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        client_id = os.getenv('GOOGLE_CLIENT_ID')
        redirect_uri = os.getenv(
            'GOOGLE_BACKEND_REDIRECT_URI', 'http://localhost:8000/api/auth/callback/'
        )

        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'access_type': 'offline',
            'prompt': 'consent',
        }

        google_auth_url = f'https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}'
        return redirect(google_auth_url)
