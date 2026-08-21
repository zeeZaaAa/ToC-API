from rest_framework import serializers

from .models import CreditCard
from shared.masked_and_pattern.pattern import (
    CREDIT_CARD_REGEX
)
from shared.masked_and_pattern.masked import (
	mask_credit_card
)

class CreditCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreditCard
        fields = ['masked_number']
        
class MaskingCreditCardCreateSerializer(serializers.ModelSerializer):
    class Meta:
            model = CreditCard
            fields = ['number']
    def validate_number(self, value):
        if not(CREDIT_CARD_REGEX.fullmatch(value)):
            raise serializers.ValidationError('Invalid credit card format')
        return value
