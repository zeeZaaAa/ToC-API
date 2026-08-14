from rest_framework import serializers

from .models import MaskingData


class MaskingDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = MaskingData
		fields = ['id']
