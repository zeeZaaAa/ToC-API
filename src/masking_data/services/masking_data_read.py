from rest_framework.pagination import PageNumberPagination

from src.masking_data.serializers import ActualDataSerializer, MaskingDataResponseSerializer


class DynamicPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


def get_masking_serializer_class(show_actual_data: bool):
    """Returns the appropriate serializer class based on the show_actual_data flag."""
    return ActualDataSerializer if show_actual_data else MaskingDataResponseSerializer
