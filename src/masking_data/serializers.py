from rest_framework import serializers

from .models import MaskingData


class MaskingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaskingData
        fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class MaskingDataCreateSerializer(serializers.Serializer):
    data = serializers.CharField(
        allow_blank=False,
        trim_whitespace=False,
    )


class MaskingDataUpdateSerializer(serializers.Serializer):
    data = serializers.CharField(
        allow_blank=False,
        trim_whitespace=False,
    )


class MaskingDataResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaskingData
        fields = [
            "id",
            "user",
            "masked_data",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class ActualDataSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    user = serializers.UUIDField(source="user.id")
    enc_data = serializers.CharField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()