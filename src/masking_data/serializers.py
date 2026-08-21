# from django.contrib.auth import get_user_model  ##################
from rest_framework import serializers
from shared.masked_and_pattern.pattern import (
	ADDRESS_REGEX,
	DOB_REGEX,
	EMAIL_REGEX,
	PHONE_NUMBER_REGEX,
)
from shared.masked_and_pattern.masked import (
	mask_address,
 	mask_dob,
	mask_phone_number,
	mask_email
)
from .models import MaskingData
# User = get_user_model() ##################################
from datetime import datetime
class MaskingDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = MaskingData
		fields = ['id']
  
class MaskingDataCreateSerializer(serializers.ModelSerializer):
    
	class Meta:
		model = MaskingData
		fields = ['email','phone_number','dob','address','credit_card']
		read_only_fields = ['credit_card','user']
	
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
				dob_date = datetime.strptime(date_str, '%d/%m/%Y').date()
				if dob_date > datetime.now().date():
					errors['dob'] = 'Date of birth cannot be in the future.'
			except ValueError:
				errors['dob'] = 'Invalid date value (e.g. day or month out of range).'
  
  
  
  
		if errors:
			raise serializers.ValidationError(errors)

		return attrs
