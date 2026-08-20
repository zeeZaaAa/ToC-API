from rest_framework import serializers
from .models import CreditCard

class MaskedCreditCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreditCard
        fields = ['masked_number']