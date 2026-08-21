from django.shortcuts import get_object_or_404

from ..models import MaskingData

# def get_masking_data_by_id(masking_data_id):
# 	return get_object_or_404(MaskingData, id=masking_data_id)

def get_masking_data_by_id(user, masking_data_id):
    return get_object_or_404(MaskingData, id=masking_data_id, user=user)

def get_user_masking_data_list(user):
    return MaskingData.objects.filter(user=user)

def update_masking_data(instance, **fields):
	for field, value in fields.items():
		setattr(instance, field, value)

	instance.save()

	return instance
