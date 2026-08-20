from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from src.credit_cards.models import CreditCard
from src.users.models import User
from .models import MaskingData
from .serializers import MaskingDataSerializer
from .serializers import ActualDataSerializer

class MaskingDataView(APIView):

	# permission_classes = [IsAuthenticated]

	def get(self, request):
		# curr_user_id = request.GET.get('user_id')

		if not request.user.is_authenticated:
			request.user = User.objects.get(id=2)

		masked_id = request.GET.get('masking_data_id')
		show_actual_data = request.GET.get('show_actual_data')
		
		if(masked_id):
			select_masked_data = get_object_or_404(MaskingData, id=masked_id, user=request.user)

			if show_actual_data and show_actual_data.lower() == 'true':
				serializer = ActualDataSerializer(select_masked_data)
			else:
				serializer = MaskingDataSerializer(select_masked_data)

			return Response(serializer.data)
		else:
			curr_user_datas = MaskingData.objects.filter(user=request.user)

			paginator = PageNumberPagination()
			paginator.page_size = 3
			result_page = paginator.paginate_queryset(curr_user_datas, request)
			
			serializer = MaskingDataSerializer(result_page, many=True)

			return paginator.get_paginated_response(serializer.data)

	def post(self, request):
		pass

	def put(self, request, id):
		pass

	def delete(self, request, id):
		pass

	def patch(self, request, id):
		pass
