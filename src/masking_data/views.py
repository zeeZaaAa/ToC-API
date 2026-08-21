from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
	MaskingDataResponseSerializer,
	MaskingDataUpdateSerializer,
)
from .services.masking_data_service import update_masking_data_service


class MaskingDataView(APIView):
	def get(self, request):
		return Response({'message': 'Response from MaskingDataView GET method'})

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
