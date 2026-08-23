from django.db import models


class CardStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    DELETED = 'DELETED', 'Deleted'
