from django.shortcuts import get_object_or_404

from ..models import MaskingData


def get_masking_data_by_id(masking_data_id):
	return get_object_or_404(MaskingData, id=masking_data_id)


def update_masking_data(instance, **fields):
	for field, value in fields.items():
		setattr(instance, field, value)

	instance.save()

	return instance
