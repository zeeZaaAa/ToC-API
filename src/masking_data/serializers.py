from rest_framework import serializers

from shared.masked_and_pattern.pattern import (
	ADDRESS_REGEX,
	CREDIT_CARD_REGEX,
	DOB_REGEX,
	EMAIL_REGEX,
	PHONE_NUMBER_REGEX,
)

from .models import MaskingData


class MaskingDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = MaskingData
		fields = ['id']


class MaskingDataUpdateSerializer(serializers.Serializer):
	email = serializers.CharField()
	phone_number = serializers.CharField()
	dob = serializers.CharField()
	address = serializers.CharField()
	credit_card = serializers.CharField()

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
		if errors:
			raise serializers.ValidationError(errors)
		return attrs


class MaskingDataResponseSerializer(serializers.ModelSerializer):
	class Meta:
		model = MaskingData
		fields = [
			'id',
			'masked_email',
			'masked_phone_number',
			'masked_dob',
			'masked_address',
			'status',
		]
