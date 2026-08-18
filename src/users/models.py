from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    login_email = models.EmailField(max_length=100, unique=True)
    oauth_token = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'login_email'
    REQUIRED_FIELDS = ['username', 'oauth_id']
    
    class Meta:
        db_table = 'users'
