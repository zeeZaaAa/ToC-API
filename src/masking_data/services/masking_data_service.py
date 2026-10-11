from uuid import UUID

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from shared.enums.masking_data import DataStatus
from shared.masked_and_pattern.masked import mask_sensitive_data
from src.masking_data.models import MaskingData
from src.masking_data.queries.masking_data_queries import (
    get_user_masking_data_list,
)


def update_masking_data_service(
    masking_data_id: UUID | str,
    user: User,
    data: dict,
) -> MaskingData:
    active_queryset = get_user_masking_data_list(user=user).exclude(status=DataStatus.DELETED)
    instance = get_object_or_404(active_queryset, id=masking_data_id)

    raw_data = data.get("data")
    if raw_data is None:
        raise ValidationError({"data": "This field is required for updates."})

    instance.enc_data = raw_data
    instance.masked_data = mask_sensitive_data(raw_data)
    instance.save()

    return instance