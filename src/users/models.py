from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	login_email = models.EmailField(max_length=100, unique=True)
	oauth_token = models.CharField(max_length=255, unique=True)

	class Meta:
		db_table = 'users'
