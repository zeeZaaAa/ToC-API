import unittest
from unittest import mock

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from src.credit_cards.models import CreditCard
from src.masking_data.models import MaskingData

try:
	from shared.masked_and_pattern.masked import mask_credit_card, mask_email

	HAS_MASK = True
except ImportError:
	HAS_MASK = False

masked_test = unittest.skipUnless(HAS_MASK, 'masked.py not yet available (Create branch)')

User = get_user_model()


class BoomError(Exception):
	pass


VALID_ADDRESS = 'Address: 123 ถนนสุขุมวิท แขวงคลองเตย เขตคลองเตย กรุงเทพมหานคร'
OLD_EMAIL = 'old@example.com'
OLD_CARD_NUMBER = '1234-1234-1234-1234'


def make_record(**overrides):
	user = User.objects.create_user(login_email='test@example.com', password='pass')
	card = CreditCard.objects.create(number=OLD_CARD_NUMBER, masked_number='1234-****-****-1234')
	defaults = {
		'user': user,
		'credit_card': card,
		'email': OLD_EMAIL,
		'phone_number': '081-234-5678',
		'dob': 'DOB:01/01/2000',
		'address': VALID_ADDRESS,
		'masked_email': 'o***@example.com',
		'masked_phone_number': '081-***-****',
		'masked_dob': 'DOB:**/01/2000',
		'masked_address': 'Address: 123 ...',
	}
	defaults.update(overrides)
	return MaskingData.objects.create(**defaults)


def full_payload(**overrides):
	payload = {
		'email': 'new@example.com',
		'phone_number': '099-999-9999',
		'dob': 'DOB:02/02/2001',
		'address': 'Address: 45/2 ซอยสุขุมวิท 22 ถนนสุขุมวิท แขวงคลองเตย เขตคลองเตย กรุงเทพมหานคร',
		'credit_card': '5555-6666-7777-8888',
	}
	payload.update(overrides)
	return payload


class MaskingDataUpdateAPITests(APITestCase):
	def setUp(self):
		self.record = make_record()
		self.url = f'/api/masking-data/{self.record.id}/'

	# ---- PUT happy path ----

	def test_put_updates_all_editable_fields(self):
		response = self.client.put(self.url, full_payload(), format='json')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.record.refresh_from_db()
		self.assertEqual(self.record.email, 'new@example.com')
		self.assertEqual(self.record.phone_number, '099-999-9999')
		self.assertEqual(self.record.dob, 'DOB:02/02/2001')
		self.assertEqual(
			self.record.address,
			'Address: 45/2 ซอยสุขุมวิท 22 ถนนสุขุมวิท แขวงคลองเตย เขตคลองเตย กรุงเทพมหานคร',
		)
		card = CreditCard.objects.get(id=self.record.credit_card_id)
		self.assertEqual(card.number, '5555-6666-7777-8888')

	# ---- PUT validation ----

	def test_put_requires_all_editable_fields(self):
		for missing in ('email', 'phone_number', 'dob', 'address', 'credit_card'):
			payload = full_payload()
			del payload[missing]
			response = self.client.put(self.url, payload, format='json')
			self.assertEqual(
				response.status_code,
				status.HTTP_400_BAD_REQUEST,
				msg=f'missing {missing} should fail',
			)
			self.assertIn(missing, response.data)

	def test_put_rejects_invalid_field_formats(self):
		cases = {
			'email': 'not-an-email',
			'phone_number': '0812345678',
			'dob': '01/01/2000',
			'address': '123 Example Road',
			'credit_card': '1234567890123456',
		}
		for field, bad_value in cases.items():
			response = self.client.put(self.url, full_payload(**{field: bad_value}), format='json')
			self.assertEqual(
				response.status_code,
				status.HTTP_400_BAD_REQUEST,
				msg=f'{field}={bad_value!r} should be rejected',
			)
			self.assertIn(field, response.data)

	# ---- PATCH happy path ----

	def test_patch_updates_single_field(self):
		for field, value in {
			'email': 'patch@example.com',
			'phone_number': '077-777-7777',
			'dob': 'DOB:03/03/2002',
			'address': 'Address: 9 ซอยสุขุมวิท 1 ถนนสุขุมวิท แขวงคลองเตยเหนือ เขตวัฒนา กรุงเทพมหานคร',
			'credit_card': '9999-8888-7777-6666',
		}.items():
			response = self.client.patch(self.url, {field: value}, format='json')
			self.assertEqual(response.status_code, status.HTTP_200_OK, msg=f'PATCH {field}')
			self.record.refresh_from_db()
			self.assertEqual(getattr(self.record, field), value, msg=f'field {field}')

	def test_patch_missing_unrelated_fields_succeeds(self):
		response = self.client.patch(self.url, {'email': 'patch@example.com'}, format='json')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.record.refresh_from_db()
		self.assertEqual(self.record.phone_number, '081-234-5678')
		self.assertEqual(self.record.dob, 'DOB:01/01/2000')
		self.assertEqual(self.record.address, VALID_ADDRESS)
		self.assertEqual(
			CreditCard.objects.get(id=self.record.credit_card_id).number, OLD_CARD_NUMBER
		)

	# ---- PATCH validation ----

	def test_patch_rejects_invalid_field_formats(self):
		for field, bad_value in {
			'email': 'not-an-email',
			'phone_number': '0812345678',
			'dob': '01/01/2000',
			'address': '123 Example Road',
			'credit_card': '1234567890123456',
		}.items():
			response = self.client.patch(self.url, {field: bad_value}, format='json')
			self.assertEqual(
				response.status_code,
				status.HTTP_400_BAD_REQUEST,
				msg=f'{field}={bad_value!r} should be rejected',
			)
			self.assertIn(field, response.data)

	# ---- 404 ----

	def test_put_returns_404_for_unknown_id(self):
		response = self.client.put('/api/masking-data/999999/', full_payload(), format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_patch_returns_404_for_unknown_id(self):
		response = self.client.patch(
			'/api/masking-data/999999/', {'email': 'x@y.com'}, format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	# ---- project-specific behavior (needs Create's masked.py) ----

	@masked_test
	def test_patch_email_regenerates_masked_email(self):
		new_email = 'patched@example.com'
		response = self.client.patch(self.url, {'email': new_email}, format='json')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.record.refresh_from_db()
		self.assertEqual(self.record.email, new_email)
		self.assertEqual(self.record.masked_email, mask_email(new_email))

	@masked_test
	def test_patch_credit_card_reuses_existing_object(self):
		card_id = self.record.credit_card_id
		new_number = '9999-8888-7777-6666'

		response = self.client.patch(self.url, {'credit_card': new_number}, format='json')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.record.refresh_from_db()
		self.assertEqual(self.record.credit_card_id, card_id)
		card = CreditCard.objects.get(id=card_id)
		self.assertEqual(card.number, new_number)
		self.assertEqual(card.masked_number, mask_credit_card(new_number))

	@masked_test
	def test_atomic_rollback_when_credit_card_save_fails(self):
		payload = full_payload(email='atomic@example.com', credit_card='4444-3333-2222-1111')

		with (
			mock.patch.object(CreditCard, 'save', side_effect=BoomError),
			self.assertRaises(BoomError),
		):
			self.client.patch(self.url, payload, format='json')

		self.record.refresh_from_db()
		self.assertEqual(self.record.email, OLD_EMAIL)
		self.assertEqual(self.record.masked_email, 'o***@example.com')
		card = CreditCard.objects.get(id=self.record.credit_card_id)
		self.assertEqual(card.number, OLD_CARD_NUMBER)
		self.assertEqual(card.masked_number, '1234-****-****-1234')
