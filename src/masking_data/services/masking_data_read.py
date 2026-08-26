from rest_framework.pagination import PageNumberPagination

from src.masking_data.serializers import ActualDataSerializer, MaskingDataResponseSerializer


def get_masking_serializer_class(show_actual_data: bool):
    if show_actual_data:
        return ActualDataSerializer
    return MaskingDataResponseSerializer


class DynamicPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10
