from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.shortcuts import get_object_or_404
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shared.enums.masking_data import DataStatus
from shared.masked_and_pattern.masked import mask_sensitive_data
from src.authentication.authentication import CustomJWTAuthentication
from src.masking_data.queries.create_masking_data import create_masking_data
from src.masking_data.queries.masking_data_queries import (
    get_user_masking_data_list,
)
from src.masking_data.services.masking_data import delete
from src.masking_data.services.masking_data_read import (
    get_masking_serializer_class,
)
from src.masking_data.services.masking_data_service import (
    update_masking_data_service,
)

from .serializers import (
    MaskingDataCreateSerializer,
    MaskingDataResponseSerializer,
    MaskingDataUpdateSerializer,
)


class DynamicPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        current_page = self.page.number
        last_page = self.page.paginator.num_pages

        prev_page = current_page - 1 if self.page.has_previous() else None
        next_page = current_page + 1 if self.page.has_next() else None

        return Response(
            {
                'data': data,
                'meta': {
                    'current_page': current_page,
                    'last_page': last_page,
                    'next_page': next_page,
                    'page_size': self.get_page_size(self.request),
                    'prev_page': prev_page,
                    'total': self.page.paginator.count,
                },
            }
        )
        
        
class MaskingDataListView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [CamelCaseJSONParser, JSONParser]

    def get(self, request):
        masking_data = get_user_masking_data_list(user=request.user)

        paginator = DynamicPageNumberPagination()
        result_page = paginator.paginate_queryset(
            masking_data,
            request,
            view=self,
        )

        if result_page is not None:
            serializer = MaskingDataResponseSerializer(
                result_page,
                many=True,
            )
            return paginator.get_paginated_response(serializer.data)

        serializer = MaskingDataResponseSerializer(
            masking_data,
            many=True,
        )

        total_count = len(serializer.data)

        return Response(
            {
                'data': serializer.data,
                'meta': {
                    'current_page': 1,
                    'last_page': 1,
                    'next_page': None,
                    'page_size': total_count,
                    'prev_page': None,
                    'total': total_count,
                },
            }
        )

    def post(self, request):
        serializer = MaskingDataCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            instance = create_masking_data(
                raw_data=serializer.validated_data['data'],
                user=request.user,
            )
        except (ValidationError, DatabaseError) as exc:
            return Response(
                {
                    'error': 'Failed to create data',
                    'details': str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                'message': 'Created successfully',
                'data': MaskingDataResponseSerializer(instance).data,
            },
            status=status.HTTP_201_CREATED,
        )


class MaskingDataView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [CamelCaseJSONParser, JSONParser]

    def get(self, request, id):
        show_actual_data = request.query_params.get('show_actual_data', '').lower() in ('true', '1')
        active_masking_data = get_user_masking_data_list(user=request.user).exclude(
            status=DataStatus.DELETED
        )
        instance = get_object_or_404(active_masking_data, id=id)

        serializer_class = get_masking_serializer_class(show_actual_data)
        serializer = serializer_class(instance, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, id):
        return self._update(request, id, partial=True)

    def _update(self, request, id, partial=False):
        serializer = MaskingDataUpdateSerializer(
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)

        if not serializer.validated_data:
            return Response(
                {'error': 'No valid fields provided for update.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance = update_masking_data_service(
            masking_data_id=id,
            user=request.user,
            data=serializer.validated_data,
        )

        return Response(
            MaskingDataResponseSerializer(instance).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request, id):
        masking_data = delete(
            masking_data_id=id,
            user=request.user,
        )

        if masking_data is None:
            return Response(
                {'message': 'Data not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                'id': masking_data.id,
                'message': 'Data was deleted successfully.',
            },
            status=status.HTTP_200_OK,
        )

class GuestMaskingDataView(APIView):
    parser_classes = [CamelCaseJSONParser, JSONParser]
    
    def post(self, request):
        data = request.data.get('data') if isinstance(request.data, dict) else None
        if not data:
            return Response(
                {'error': 'Field "data" is required.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        masked_text = mask_sensitive_data(data)
        return Response({'masked_text': masked_text})