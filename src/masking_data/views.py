from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from src.credit_cards.models import CreditCard

from .models import MaskingData
from .serializers import (
	MaskingDataResponseSerializer,
	MaskingDataSerializer,
	MaskingDataUpdateSerializer,
)
from .services.masking_data_service import update_masking_data_service


class MaskingDataView(APIView):
	def get(self, request):
		curr_user_id = request.GET.get('id')
		curr_user_datas = get_object_or_404(MaskingData, id=curr_user_id)
		curr_user_credit_cards = get_object_or_404(CreditCard, id=curr_user_datas.credit_card)

		serializer = MaskingDataSerializer(curr_user_datas, curr_user_credit_cards)
		return Response(serializer.data)

	def post(self, request):
		pass

	def put(self, request, id):
		serializer = MaskingDataUpdateSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		instance = update_masking_data_service(id, serializer.validated_data)
		return Response(MaskingDataResponseSerializer(instance).data)

	def delete(self, request, id):
		pass

	def patch(self, request, id):
		serializer = MaskingDataUpdateSerializer(data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		instance = update_masking_data_service(id, serializer.validated_data)
		return Response(MaskingDataResponseSerializer(instance).data)
