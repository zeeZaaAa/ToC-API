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
from .services import DynamicPageNumberPagination
from . import queries, services

class MaskingDataListView(APIView):

	permission_classes = [IsAuthenticated]

	def get(self, request):
		curr_user_datas = queries.get_user_masking_data_list(user=request.user)

		paginator = DynamicPageNumberPagination()
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


class MaskingDataDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        show_actual_data = request.GET.get('show_actual_data')
        
        select_masked_data = queries.get_masking_data_by_id(user=request.user, masking_data_id=id)
        SerializerClass = services.get_masking_serializer_class(show_actual_data)
        
        serializer = SerializerClass(select_masked_data)
        return Response(serializer.data)

    def put(self, request, id):
        pass

    def patch(self, request, id):
        pass

    def delete(self, request, id):
        pass