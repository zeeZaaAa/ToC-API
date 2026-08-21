from datetime import datetime

from rest_framework import serializers

from shared.masked_and_pattern.pattern import (
	ADDRESS_REGEX,
	CREDIT_CARD_REGEX,
	DOB_REGEX,
	EMAIL_REGEX,
	PHONE_NUMBER_REGEX,
)
from src.credit_cards.models import CreditCard

from .models import MaskingData


class MaskingDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = MaskingData
		fields = ['id']


class MaskingDataUpdateSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=255)
	phone_number = serializers.CharField(max_length=50)
	dob = serializers.CharField(max_length=50)
	address = serializers.CharField(max_length=500)
	credit_card = serializers.CharField(max_length=100)

	def validate(self, attrs):
		errors = {}
		checks = (
			('email', EMAIL_REGEX, 'Invalid email format.'),
			('phone_number', PHONE_NUMBER_REGEX, 'Invalid phone number format.'),
			('dob', DOB_REGEX, 'Invalid date of birth format.'),
			('address', ADDRESS_REGEX, 'Invalid address format.'),
			('credit_card', CREDIT_CARD_REGEX, 'Invalid credit card format.'),
		)
		for field, regex, message in checks:
			if field in attrs and not regex.fullmatch(attrs[field]):
				errors[field] = message
		if 'dob' in attrs and 'dob' not in errors:
			try:
				# ponytail: calendar-validity check only; timezone is intentionally irrelevant
				datetime.strptime(attrs['dob'], 'DOB:%d/%m/%Y')  # noqa: DTZ007
			except ValueError:
				errors['dob'] = 'Invalid date of birth.'
		if errors:
			raise serializers.ValidationError(errors)
		return attrs


class MaskedCreditCardSerializer(serializers.ModelSerializer):
	class Meta:
		model = CreditCard
		fields = ['id', 'masked_number']


class MaskingDataResponseSerializer(serializers.ModelSerializer):
	credit_card = MaskedCreditCardSerializer(read_only=True)

	class Meta:
		model = MaskingData
		fields = [
			'id',
			'masked_email',
			'masked_phone_number',
			'masked_dob',
			'masked_address',
			'status',
			'credit_card',
		]
