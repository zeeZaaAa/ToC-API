from typing import TypedDict

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

User = get_user_model()


class OAuthUserData(TypedDict):
    email: str
    google_id: str


class UserService:
    """Handles direct database persistence and retrieval for User domain."""

    @staticmethod
    def get_or_create_oauth_user(user_data: OAuthUserData) -> AbstractBaseUser:
        user, _ = User.objects.get_or_create(
            email=user_data['email'],
            defaults={
                'google_id': user_data['google_id'],
            },
        )
        return user
