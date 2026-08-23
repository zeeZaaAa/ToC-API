from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

User = get_user_model()


class UserService:
    """Handles direct database persistence and retrieval for User domain."""

    @staticmethod
    def get_or_create_oauth_user(user_data: dict[str, Any]) -> AbstractBaseUser:
        user, _ = User.objects.get_or_create(
            login_email=user_data['email'],
            defaults={
                'oauth_id': user_data['oauth_id'],
                'username': user_data['username'],
            },
        )
        return user