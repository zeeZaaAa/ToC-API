from uuid import UUID

from django.contrib.auth.models import User
from django.db import transaction

from shared.enums.masking_data import DataStatus

from ..models import MaskingData
from ..queries import masking_data as masking_data_queries


def delete(masking_data_id: UUID | str, user: User) -> MaskingData | None:
    masking_data = MaskingData.objects.filter(id=masking_data_id, user=user).first()

    if masking_data is None or masking_data.status == DataStatus.DELETED:
        return None

    with transaction.atomic():
        masking_data_queries.set_status(masking_data, DataStatus.DELETED)

    return masking_data