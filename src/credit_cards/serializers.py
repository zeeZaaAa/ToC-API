from rest_framework import serializers

from shared.masked_and_pattern.pattern import CREDIT_CARD_REGEX

from .models import CreditCard


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
