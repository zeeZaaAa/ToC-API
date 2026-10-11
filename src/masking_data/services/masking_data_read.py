from src.masking_data.serializers import ActualDataSerializer, MaskingDataResponseSerializer


def get_masking_serializer_class(show_actual_data: bool):
    """Returns the appropriate serializer class based on the show_actual_data flag."""
    return ActualDataSerializer if show_actual_data else MaskingDataResponseSerializer
