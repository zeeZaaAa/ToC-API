from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, login_email, password=None, **extra_fields):
        if not login_email:
            raise ValueError('The Email field must be set')
        login_email = self.normalize_email(login_email)
        user = self.model(login_email=login_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login_email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(login_email, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    login_email = models.EmailField(max_length=100, unique=True)
    oauth_id = models.CharField(max_length=255, unique=True, blank=True, null=True)

    USERNAME_FIELD = 'login_email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'

