from rest_framework.pagination import PageNumberPagination

from src.masking_data.serializers import ActualDataSerializer, MaskingDataSerializer


def get_masking_serializer_class(show_actual_data: str):
    if show_actual_data and show_actual_data.lower() == 'true':
        return ActualDataSerializer
    return MaskingDataSerializer

class DynamicPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size' 
    max_page_size = 10