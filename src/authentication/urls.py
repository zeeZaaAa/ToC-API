from django.urls import path

from .views import (
    CookieTokenRefreshView,
    GoogleCallbackView,
    GoogleOAuthUrlView,
    LogoutView,
    ProtectedProfileView,
)

urlpatterns = [
    path('google-url/', GoogleOAuthUrlView.as_view(), name='google_oauth_url'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', ProtectedProfileView.as_view(), name='protected_profile'),
    path('callback/', GoogleCallbackView.as_view(), name='google-callback'),
]
