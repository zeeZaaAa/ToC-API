from django.shortcuts import get_object_or_404

from shared.masked_and_pattern.masked import mask_sensitive_data
from src.masking_data.models import MaskingData


def update_masking_data_service(
    masking_data_id,
    user,
    data,
):
    instance = get_object_or_404(
        MaskingData,
        id=masking_data_id,
        user=user,
    )

    raw_data = data.get("data")
    if raw_data is not None:
        instance.enc_data = raw_data
        instance.masked_data = mask_sensitive_data(raw_data)

    instance.save()

    return instance