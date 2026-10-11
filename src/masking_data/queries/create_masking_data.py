from django.db import transaction

from shared.masked_and_pattern.masked import mask_sensitive_data
from src.masking_data.models import MaskingData


def create_masking_data(raw_data: str, user) -> MaskingData:
    """Creates a new MaskingData record, automatically generating masked_data."""
    masked_text = mask_sensitive_data(raw_data)

    with transaction.atomic():
        masking_record = MaskingData.objects.create(
            user=user,
            enc_data=raw_data,
            masked_data=masked_text,
        )

        return masking_record