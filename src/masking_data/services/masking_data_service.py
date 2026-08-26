from django.shortcuts import get_object_or_404

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

    for field, value in data.items():
        setattr(instance, field, value)

    instance.save()

    return instance