# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CreditCard
from .serializers import CreditCardSerializer


@api_view(['GET'])
def get_masked_credit_card_number_by_id(request):

    credit_card_id = request.GET.get('id')
    credit_card_details = get_object_or_404(CreditCard, id=credit_card_id)

    serializer = CreditCardSerializer(credit_card_details)

    return Response(serializer.data)

class MaskingDataView(APIView):
    def post(self, request):
        pass