from rest_framework import serializers

from .models import MaskingData
from src.credit_cards.serializers import MaskedCreditCardSerializer

class MaskingDataSerializer(serializers.ModelSerializer):

	credit_card = MaskedCreditCardSerializer(read_only=True)

	class Meta:
		model = MaskingData
		fields = [
			'id', 
			'user', 
			'credit_card', 
			'masked_email', 
			'masked_phone_number', 
			'masked_dob', 
			'masked_address'
			]
		
class ActualDataSerializer(serializers.ModelSerializer):

	credit_card = MaskedCreditCardSerializer(read_only=True)

	class Meta:
		model = MaskingData
		fields = [
			'id', 
			'user', 
			'credit_card', 
			'email', 
			'phone_number', 
			'dob', 
			'address'
			]
		