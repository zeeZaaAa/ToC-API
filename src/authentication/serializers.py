from rest_framework import serializers


class OAuthLoginSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=['google'])
    code = serializers.CharField(required=True)
    redirect_uri = serializers.CharField(required=False, allow_blank=True, default=None)