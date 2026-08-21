from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from src.credit_cards.models import CreditCard
from src.credit_cards.serializers import MaskingCreditCardCreateSerializer
from .models import MaskingData
from .serializers import MaskingDataCreateSerializer, MaskingDataSerializer
from django.db import transaction
from src.masking_data.query.create_masking_data import create_masking_data


class MaskingDataView(APIView):
	def get(self, request):
		curr_user_id = request.GET.get('id')
		curr_user_datas = get_object_or_404(MaskingData, id=curr_user_id)
		curr_user_credit_cards = get_object_or_404(CreditCard, id=curr_user_datas.credit_card)

		serializer = MaskingDataSerializer(curr_user_datas, curr_user_credit_cards)
		return Response(serializer.data)

	def post(self, request):
     
		user = request.user
		card_serializer = MaskingCreditCardCreateSerializer(data=request.data.get('credit_card', {}))
		masking_data_serializer = MaskingDataCreateSerializer(data=request.data)
		card_serializer = MaskingCreditCardCreateSerializer(data=request.data.get('credit_card'))
		masking_data_serializer = MaskingDataCreateSerializer(data=request.data)
  
		if not card_serializer.is_valid():
			return Response(card_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		if not masking_data_serializer.is_valid():
			return Response(masking_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		try:
			create_masking_data(card_data=card_serializer.validated_data,masking_data=masking_data_serializer.validated_data,user=user)
		except Exception as e:
			return Response(
                {"error": "Failed to create data", "details": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
		return Response({
            "message": "Created successfully",
        }, status=status.HTTP_201_CREATED)
		

	def put(self, request, id):
		pass

	def delete(self, request, id):
		pass

	def patch(self, request, id):
		pass
