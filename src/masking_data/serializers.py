from rest_framework import serializers
from .models import MaskingData
from shared.masked_and_pattern.pattern import (
    EMAIL_REGEX,
    PHONE_NUMBER_REGEX,
    DOB_REGEX,
    ADDRESS_REGEX,
    CREDIT_CARD_REGEX
    )


class MaskingDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = MaskingData
		fields = ['id']
class MaskingDataCreateSerializer(serializers.ModelSerializer):
    
	class Meta:
		model = MaskingData
		fields = ['email','phone_number','dob','address','credit_card']

	
	def validate(self, attrs):
		errors = {}

		if not EMAIL_REGEX.fullmatch(attrs.get('email', '')):
			errors['email'] = 'Invalid email format.'
		if not PHONE_NUMBER_REGEX.fullmatch(attrs.get('phone_number', '')):
			errors['phone_number'] = 'Invalid phone number format.'
		if not CREDIT_CARD_REGEX.fullmatch(attrs.get('credit_card', '')):
			errors['credit_card'] = 'Invalid credit card format.'
		if not ADDRESS_REGEX.fullmatch(attrs.get('address', '')):
			errors['address'] = 'Invalid address format.'
		if not DOB_REGEX.fullmatch(attrs.get('dob', '')):
			errors['dob'] = 'Invalid date of birth format.'

		if errors:
			raise serializers.ValidationError(errors)

		return attrs
	
    
