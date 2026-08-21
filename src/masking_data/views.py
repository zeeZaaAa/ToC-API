from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from shared.enums.credit_card import CardStatus
from shared.enums.masking_data import DataStatus

from .models import MaskingData


class MaskingDataView(APIView):
	def get(self, request, id=None):
		return Response({'message': 'Response from MaskingDataView GET method'})

	def post(self, request):
		pass

	def put(self, request, id):
		pass

	def delete(self, request, id):
		masking_data = get_object_or_404(MaskingData, id=id)

		if masking_data.status == DataStatus.DELETED:
			return Response(
				{'message': 'This data has already been deleted.'}, status=status.HTTP_410_GONE
			)

		with transaction.atomic():
			masking_data.status = DataStatus.DELETED
			masking_data.save(update_fields=['status', 'updated_at'])
			credit_card = masking_data.credit_card
			# has_active = credit_card.masking_datas.filter(status=DataStatus.ACTIVE).exists()
			# if not has_active and credit_card.status != CardStatus.DELETED:
			if credit_card.status != CardStatus.DELETED:
				credit_card.status = CardStatus.DELETED
				credit_card.save(update_fields=['status'])

		return Response(
			{'id': masking_data.id, 'message': 'Data was deleted successfully.'},
			status=status.HTTP_200_OK,
		)

	def patch(self, request, id):
		pass
