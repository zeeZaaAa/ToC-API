from django.db import transaction

from shared.enums.credit_card import CardStatus
from shared.enums.masking_data import DataStatus
from src.credit_cards.queries import credit_card as credit_card_queries

from ..models import MaskingData
from ..queries import masking_data as masking_data_queries


def delete(id: int) -> MaskingData | None:
	masking_data = masking_data_queries.get_by_id(id)

	if masking_data is None or masking_data.status == DataStatus.DELETED:
		return None

	with transaction.atomic():
		masking_data_queries.set_status(masking_data, DataStatus.DELETED)
		credit_card = masking_data.credit_card
		# if not credit_card_queries.has_active_masking_data(credit_card):
		if credit_card.status != CardStatus.DELETED:
			credit_card_queries.set_status(credit_card, CardStatus.DELETED)

	return masking_data
