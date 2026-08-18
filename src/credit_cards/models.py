from django.core.exceptions import PermissionDenied
from django.db import models

from shared.enums.credit_card import CardStatus


class CreditCard(models.Model):
	number = models.TextField()
	masked_number = models.TextField()
	status = models.CharField(max_length=20, choices=CardStatus.choices, default=CardStatus.ACTIVE)

	class Meta:
		db_table = 'credit_cards'

	def delete(self, *args, **kwargs):
		if not kwargs.pop('is_cascade', False):
			raise PermissionDenied(
				'CreditCard cannot be deleted directly. '
				'Delete the associated MaskingData record instead.'
			)
		super().delete(*args, **kwargs)
