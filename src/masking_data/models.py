from django.core.exceptions import PermissionDenied
from django.db import models

from ...shared.enums.masking_data import DataStatus
from ...src.credit_cards.models import CreditCard
from ...src.users.models import User


class MaskingData(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='masking_datas')
	credit_card = models.ForeignKey(
		CreditCard, on_delete=models.CASCADE, related_name='masking_datas'
	)

	email = models.TextField()
	phone_number = models.TextField()
	dob = models.TextField()
	address = models.TextField()

	masked_email = models.TextField()
	masked_phone_number = models.TextField()
	masked_dob = models.TextField()
	masked_address = models.TextField()

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=20, choices=DataStatus.choices, default=DataStatus.ACTIVE)

	class Meta:
		db_table = 'masking_datas'

	def delete(self, *args, **kwargs):
		if not kwargs.pop('is_cascade', False):
			raise PermissionDenied('MaskingData cannot be deleted directly.')
		super().delete(*args, **kwargs)
