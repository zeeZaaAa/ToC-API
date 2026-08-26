from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from src.masking_data.serializers import ActualDataSerializer, MaskingDataResponseSerializer


class DynamicPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


def get_masking_serializer_class(show_actual_data: bool):
    """Returns the appropriate serializer class based on the show_actual_data flag."""
    return ActualDataSerializer if show_actual_data else MaskingDataResponseSerializer


def get_paginated_masking_response(queryset, request, view, show_actual_data: bool) -> Response:
    """Paginates a queryset using DynamicPageNumberPagination and serializes it

    with the dynamic serializer class.
    """
    paginator = DynamicPageNumberPagination()
    page = paginator.paginate_queryset(queryset, request, view=view)
    
    serializer_class = get_masking_serializer_class(show_actual_data)

    if page is not None:
        serializer = serializer_class(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True, context={'request': request})
    return Response(serializer.data)