from ..models import MaskingData


def get_by_id(id: int) -> MaskingData | None:
    return MaskingData.objects.filter(id=id).first()


def set_status(masking_data: MaskingData, status: str) -> None:
    masking_data.status = status
    masking_data.save(update_fields=['status', 'updated_at'])
