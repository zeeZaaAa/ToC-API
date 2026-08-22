from src.credit_cards.models import CreditCard
from shared.masked_and_pattern.masked import mask_credit_card

def create_credit_card(number: str) -> CreditCard:
    masked_number = mask_credit_card(number)
    return CreditCard.objects.create(
        number=number,
        masked_number=masked_number
    )