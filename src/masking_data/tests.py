# Create your tests here.
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.credit_cards.models import CreditCard
from .models import MaskingData
from .serializers import MaskingDataCreateSerializer, MaskingDataSerializer

User = get_user_model()


class MaskingDataModelTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.credit_card = CreditCard.objects.create(user=self.user)
        self.masking_data = MaskingData.objects.create(
            user=self.user,
            credit_card=self.credit_card,
            email="test@example.com",
            phone_number="0812345678",
            dob="1995-01-01",
            address="123 Bangkok",
            masked_email="t***@example.com",
            masked_phone_number="081****678",
            masked_dob="****-**-**",
            masked_address="123 *******",
        )

    def test_direct_delete_raises_permission_denied(self):
        """ไม่อนุญาตให้ลบข้อมูลโดยตรงผ่าน .delete()"""
        with self.assertRaises(PermissionDenied):
            self.masking_data.delete()

    def test_cascade_delete_allowed(self):
        """อนุญาตให้ลบได้หากส่ง kwargs is_cascade=True"""
        self.masking_data.delete(is_cascade=True)
        self.assertEqual(MaskingData.objects.count(), 0)


class MaskingDataSerializerTests(APITestCase):
    @patch("your_app.serializers.EMAIL_REGEX")
    @patch("your_app.serializers.PHONE_NUMBER_REGEX")
    @patch("your_app.serializers.ADDRESS_REGEX")
    @patch("your_app.serializers.DOB_REGEX")
    def test_validation_failed(self, mock_dob, mock_address, mock_phone, mock_email):
        """ทดสอบกรณี Regex match ไม่ผ่านทุกฟิลด์"""
        mock_email.fullmatch.return_value = False
        mock_phone.fullmatch.return_value = False
        mock_address.fullmatch.return_value = False
        mock_dob.fullmatch.return_value = False

        data = {
            "email": "invalid-email",
            "phone_number": "invalid-phone",
            "dob": "invalid-dob",
            "address": "invalid-address",
        }
        serializer = MaskingDataCreateSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.assertIn("phone_number", serializer.errors)
        self.assertIn("address", serializer.errors)
        self.assertIn("dob", serializer.errors)

    @patch("your_app.serializers.mask_email", return_value="m***@mail.com")
    @patch("your_app.serializers.mask_phone_number", return_value="081****567")
    @patch("your_app.serializers.mask_dob", return_value="****-01-01")
    @patch("your_app.serializers.mask_address", return_value="*** BKK")
    @patch("your_app.serializers.EMAIL_REGEX")
    @patch("your_app.serializers.PHONE_NUMBER_REGEX")
    @patch("your_app.serializers.ADDRESS_REGEX")
    @patch("your_app.serializers.DOB_REGEX")
    def test_create_new_masked_success(
        self,
        mock_dob_regex,
        mock_addr_regex,
        mock_phone_regex,
        mock_email_regex,
        mock_mask_addr,
        mock_mask_dob,
        mock_mask_phone,
        mock_mask_email,
    ):
        """ทดสอบฟังก์ชัน create_new_masked ว่าแปลงข้อมูลตามฟังก์ชัน mask ถูกต้อง"""
        mock_email_regex.fullmatch.return_value = True
        mock_phone_regex.fullmatch.return_value = True
        mock_addr_regex.fullmatch.return_value = True
        mock_dob_regex.fullmatch.return_value = True

        data = {
            "email": "myemail@mail.com",
            "phone_number": "0812345567",
            "dob": "2000-01-01",
            "address": "123 BKK",
        }
        serializer = MaskingDataCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        masked_result = serializer.create_new_masked(serializer.validated_data)
        self.assertEqual(masked_result["masked_email"], "m***@mail.com")
        self.assertEqual(masked_result["masked_phone_number"], "081****567")
        self.assertEqual(masked_result["masked_dob"], "****-01-01")
        self.assertEqual(masked_result["masked_address"], "*** BKK")


class MaskingDataViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("masking-data")  # เปลี่ยนชื่อตามที่ตั้งใน urls.py
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.credit_card = CreditCard.objects.create(user=self.user)
        self.masking_data = MaskingData.objects.create(
            user=self.user,
            credit_card=self.credit_card,
            email="test@example.com",
            phone_number="0812345678",
            dob="1995-01-01",
            address="123 Bangkok",
        )

    def test_get_masking_data_success(self):
        """ทดสอบ GET MaskingData ด้วย ID ที่มีอยู่จริง"""
        response = self.client.get(self.url, {"id": self.masking_data.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.masking_data.id)

    def test_get_masking_data_not_found(self):
        """ทดสอบ GET ด้วย ID ที่ไม่มีอยู่ในระบบ (Expected 404)"""
        response = self.client.get(self.url, {"id": 99999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("your_app.serializers.EMAIL_REGEX")
    @patch("your_app.serializers.PHONE_NUMBER_REGEX")
    @patch("your_app.serializers.ADDRESS_REGEX")
    @patch("your_app.serializers.DOB_REGEX")
    def test_post_masking_data_validation_error(
        self, mock_dob, mock_address, mock_phone, mock_email
    ):
        """ทดสอบ POST ข้อมูลที่ไม่ผ่าน Validation (Expected 400)"""
        mock_email.fullmatch.return_value = False
        mock_phone.fullmatch.return_value = True
        mock_address.fullmatch.return_value = True
        mock_dob.fullmatch.return_value = True

        payload = {
            "email": "bad-email",
            "phone_number": "0812345678",
            "dob": "1995-01-01",
            "address": "Bangkok",
        }
        response = self.client.post(self.url, payload, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)