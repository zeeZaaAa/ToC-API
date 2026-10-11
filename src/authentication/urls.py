from django.urls import path

from .views import (
    CookieTokenRefreshView,
    GoogleCallbackView,
    GoogleLoginRedirectView,
    LogoutView,
    ProtectedProfileView,
)

urlpatterns = [
    path('login/', GoogleLoginRedirectView.as_view(), name='google-login'),
    path('callback/', GoogleCallbackView.as_view(), name='google-callback'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', ProtectedProfileView.as_view(), name='protected_profile'),
]
