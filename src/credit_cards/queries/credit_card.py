from shared.enums.masking_data import DataStatus

from ..models import CreditCard


def set_status(credit_card: CreditCard, status: str) -> None:
    credit_card.status = status
    credit_card.save(update_fields=['status'])


def has_active_masking_data(credit_card: CreditCard) -> bool:
    return credit_card.masking_datas.filter(status=DataStatus.ACTIVE).exists()
