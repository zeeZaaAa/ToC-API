from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import masking_data as masking_data_service


class MaskingDataView(APIView):
	def get(self, request, id=None):
		return Response({'message': 'Response from MaskingDataView GET method'})

	def post(self, request):
		pass

	def put(self, request, id):
		pass

	def delete(self, request, id):
		masking_data = masking_data_service.delete(id)

		if masking_data is None:
			return Response({'message': 'Data not found.'}, status=status.HTTP_404_NOT_FOUND)

		return Response(
			{'id': masking_data.id, 'message': 'Data was deleted successfully.'},
			status=status.HTTP_200_OK,
		)

	def patch(self, request, id):
		pass
