from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shared.enums.masking_data import DataStatus
from src.authentication.authentication import CustomJWTAuthentication
from src.masking_data.queries.create_masking_data import create_masking_data
from src.masking_data.queries.masking_data_queries import (
    get_user_masking_data_list,
)
from src.masking_data.services.masking_data import delete
from src.masking_data.services.masking_data_read import (
    DynamicPageNumberPagination,
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


class MaskingDataListView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

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

        return Response(serializer.data)

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

    def get(self, request, id):
        show_actual_data = request.query_params.get('show_actual_data', '').lower() in ('true', '1')
        active_masking_data = get_user_masking_data_list(user=request.user).exclude(status=DataStatus.DELETED)
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
