from django.db import models


class DataStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    DELETED = 'DELETED', 'Deleted'
