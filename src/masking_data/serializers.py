from datetime import datetime, timezone

from django.utils import timezone as django_timezone
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
                datetime.strptime(attrs['dob'], 'DOB:%d/%m/%Y').replace(tzinfo=timezone.utc)
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
            'user',
            'masked_email',
            'masked_phone_number',
            'masked_dob',
            'masked_address',
            'credit_card',
            'created_at',
            'updated_at',
        ]


class MaskingDataCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaskingData
        fields = ['email', 'phone_number', 'dob', 'address', 'credit_card']
        read_only_fields = ['credit_card', 'user']

    def validate(self, attrs):
        errors = {}

        if not EMAIL_REGEX.fullmatch(attrs.get('email', '')):
            errors['email'] = 'Invalid email format.'
        if not PHONE_NUMBER_REGEX.fullmatch(attrs.get('phone_number', '')):
            errors['phone_number'] = 'Invalid phone number format.'
        if not ADDRESS_REGEX.fullmatch(attrs.get('address', '')):
            errors['address'] = 'Invalid address format.'
        if not DOB_REGEX.fullmatch(attrs.get('dob', '')):
            errors['dob'] = 'Invalid date of birth format.'
        else:
            raw_dob = attrs.get('dob', '')
            date_str = raw_dob.replace('DOB:', '').strip()
            try:
                dob_date = (
                    datetime.strptime(date_str, '%d/%m/%Y').replace(tzinfo=timezone.utc).date()
                )
                if dob_date > django_timezone.localdate():
                    errors['dob'] = 'Date of birth cannot be in the future.'
            except ValueError:
                errors['dob'] = 'Invalid date value (e.g. day or month out of range).'

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


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
            'address',
            'created_at',
            'updated_at',
        ]
