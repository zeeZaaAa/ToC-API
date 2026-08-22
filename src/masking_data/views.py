from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ActualDataSerializer
from .services import DynamicPageNumberPagination
from rest_framework.permissions import IsAuthenticated

from src.credit_cards.models import CreditCard
from src.credit_cards.serializers import MaskingCreditCardCreateSerializer
from src.masking_data.queries.create_masking_data import create_masking_data
from .models import MaskingData
from .serializers import MaskingDataCreateSerializer, MaskingDataSerializer
from django.db import transaction
from .serializers import ActualDataSerializer
from rest_framework.permissions import IsAuthenticated

from .models import MaskingData
from .serializers import (
	MaskingDataCreateSerializer,
	MaskingDataResponseSerializer,
	MaskingDataSerializer,
	MaskingDataUpdateSerializer,
	MaskingDataSerializer,
)

from src.masking_data.queries.masking_data_queries import(
    get_masking_data_by_id,
    get_user_masking_data_list,
)

from src.masking_data.services.masking_data_read import(
    get_masking_serializer_class,
    DynamicPageNumberPagination,
)
from .services.masking_data_service import update_masking_data_service
from django.shortcuts import get_object_or_404
from rest_framework import status
from src.credit_cards.models import CreditCard
from src.credit_cards.serializers import MaskingCreditCardCreateSerializer
from .models import MaskingData
from .serializers import MaskingDataCreateSerializer, MaskingDataSerializer
from django.db import transaction
from src.masking_data.queries.create_masking_data import create_masking_data
from .services import masking_data as masking_data_service
from .services.masking_data_service import update_masking_data_service
from .services.masking_data_service import (
    update_masking_data_service,
    get_masking_serializer_class,
                                            )

from src.masking_data.queries.masking_data_queries import (
	get_masking_data_by_id,
	update_masking_data,
    get_user_masking_data_list,
)

class MaskingDataListView(APIView):

	permission_classes = [IsAuthenticated]

	def get(self, request):
		curr_user_datas = get_user_masking_data_list(user=request.user)

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

class MaskingDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        show_actual_data = request.GET.get('show_actual_data')
        
        select_masked_data = get_masking_data_by_id(user=request.user, masking_data_id=id)
        SerializerClass = get_masking_serializer_class(show_actual_data)
        
        serializer = SerializerClass(select_masked_data)
        return Response(serializer.data)
    
    def post(self, request):
        user = request.user
        card_serializer = MaskingCreditCardCreateSerializer(
			data=request.data.get('credit_card', {})
		)
        masking_data_serializer = MaskingDataCreateSerializer(data=request.data)

        is_card_valid = card_serializer.is_valid()
        is_masking_valid = masking_data_serializer.is_valid()

        if not (is_card_valid and is_masking_valid):
            errors = {}
            if not is_card_valid:
                errors['credit_card'] = card_serializer.errors
            if not is_masking_valid:
                errors.update(masking_data_serializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            create_masking_data(
				card_data=card_serializer.validated_data,
				masking_data=masking_data_serializer.validated_data,
				user=user,
			)
        except (ValidationError, DatabaseError) as e:
            return Response(
				{'error': 'Failed to create data', 'details': str(e)},
				status=status.HTTP_400_BAD_REQUEST,
			)
        return Response({'message': 'Created successfully'}, status=status.HTTP_201_CREATED)

    def put(self, request, id):
        serializer = MaskingDataUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = update_masking_data_service(id, serializer.validated_data)
        return Response(MaskingDataResponseSerializer(instance).data)

    def delete(self, request, id):
        masking_data = masking_data_service.delete(id)

        if masking_data is None:
            return Response({'message': 'Data not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(
			{'id': masking_data.id, 'message': 'Data was deleted successfully.'},
			status=status.HTTP_200_OK,
		)

    def patch(self, request, id):
        serializer = MaskingDataUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = update_masking_data_service(id, serializer.validated_data)
        return Response(MaskingDataResponseSerializer(instance).data)
        pass
    
