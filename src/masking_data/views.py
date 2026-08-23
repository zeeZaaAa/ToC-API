from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.authentication.authentication import CustomJWTAuthentication
from src.credit_cards.models import CreditCard
from src.credit_cards.serializers import MaskingCreditCardCreateSerializer
from src.masking_data.queries.create_masking_data import create_masking_data

from .models import MaskingData
from .serializers import (
	MaskingDataCreateSerializer,
	MaskingDataResponseSerializer,
	MaskingDataSerializer,
	MaskingDataUpdateSerializer,
)
from .services import masking_data as masking_data_service
from .services.masking_data_service import update_masking_data_service


class MaskingDataListView(APIView):

	permission_classes = [IsAuthenticated]

class MaskingDataView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        curr_user_id = request.GET.get('id')
        if not curr_user_id:
            return Response(
                {'error': 'id parameter is required'}, status=status.HTTP_400_BAD_REQUEST
            )

        curr_user_datas = get_object_or_404(MaskingData, id=curr_user_id, user=request.user)
        curr_user_credit_cards = get_object_or_404(CreditCard, id=curr_user_datas.credit_card_id)

        serializer = MaskingDataSerializer(curr_user_datas, curr_user_credit_cards)
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
        get_object_or_404(MaskingData, id=id, user=request.user)

        serializer = MaskingDataUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = update_masking_data_service(id, serializer.validated_data)
        return Response(MaskingDataResponseSerializer(instance).data)

    def delete(self, request, id):
        get_object_or_404(MaskingData, id=id, user=request.user)

        masking_data = masking_data_service.delete(id)
        if masking_data is None:
            return Response({'message': 'Data not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {'id': masking_data.id, 'message': 'Data was deleted successfully.'},
            status=status.HTTP_200_OK,
        )

    def patch(self, request, id):
        get_object_or_404(MaskingData, id=id, user=request.user)

        serializer = MaskingDataUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = update_masking_data_service(id, serializer.validated_data)
        return Response(MaskingDataResponseSerializer(instance).data)
