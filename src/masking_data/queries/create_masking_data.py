from django.db import transaction
from src.credit_cards.models import CreditCard
from src.masking_data.models import MaskingData
from src.credit_cards.queries.create_credit_card import create_credit_card
from shared.masked_and_pattern.masked import (
    mask_email,
    mask_phone_number,
    mask_dob,
    mask_address
)

def create_masking_data(card_data: dict, masking_data: dict,user) -> MaskingData:

    with transaction.atomic():
        credit_card = create_credit_card(**card_data)
        masking_record = MaskingData.objects.create(
            user=user,
            credit_card=credit_card,
            email=masking_data['email'],
            phone_number=masking_data['phone_number'],
            dob=masking_data['dob'],
            address=masking_data['address'],
            masked_email=mask_email(masking_data['email']),
            masked_phone_number=mask_phone_number(masking_data['phone_number']),
            masked_dob=mask_dob(masking_data['dob']),
            masked_address=mask_address(masking_data['address'])
        )

        return masking_record