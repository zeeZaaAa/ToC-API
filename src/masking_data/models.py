import uuid

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import models
from encrypted_model_fields.fields import EncryptedTextField

from shared.enums.masking_data import DataStatus


class MaskingData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='masking_datas'
    )
    
    enc_data = EncryptedTextField()
    masked_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=DataStatus.choices, default=DataStatus.ACTIVE)

    class Meta:
        db_table = 'masking_datas'

    def delete(self, *args, **kwargs):
        if not kwargs.pop('is_cascade', False):
            raise PermissionDenied('MaskingData cannot be deleted directly.')
        super().delete(*args, **kwargs)
