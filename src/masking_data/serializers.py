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

	def update(self, instance, validated_data):
		# Lazy import: mask functions are provided by the Create branch.
		from shared.masked_and_pattern.masked import (
			mask_address,
			mask_credit_card,
			mask_dob,
			mask_email,
			mask_phone_number,
		)

		masked_by_field = {
			'email': 'masked_email',
			'phone_number': 'masked_phone_number',
			'dob': 'masked_dob',
			'address': 'masked_address',
		}
		mask_by_field = {
			'email': mask_email,
			'phone_number': mask_phone_number,
			'dob': mask_dob,
			'address': mask_address,
		}
		for field, mask_fn in mask_by_field.items():
			if field in validated_data:
				setattr(instance, field, validated_data[field])
				setattr(instance, masked_by_field[field], mask_fn(validated_data[field]))

		credit_card = instance.credit_card
		if 'credit_card' in validated_data:
			credit_card.number = validated_data['credit_card']
			credit_card.masked_number = mask_credit_card(validated_data['credit_card'])

		instance.save()
		if 'credit_card' in validated_data:
			credit_card.save()
		return instance
