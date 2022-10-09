from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


# Create your tests here.


class UserTests(TestCase):
    """
        Test module for User model
    """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            phone='+998900112116',
            full_name='Test User',
            otp='1234',
            phone2='+998939036903',
            is_verified=False
        )
        self.user.set_password('testpass')
        self.user.save()

    def test_create_user(self):
        url = reverse('user-create')
        data = {
            'phone': '+998900112116',
            'full_name': 'Test User',
            'otp': '1234',
            'phone2': '+998939036903',
            'is_verified': False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 2)
        self.assertEqual(get_user_model().objects.get().phone, '+998900112116')

    def test_verify_user(self):
        url = reverse('user-verify')
        data = {
            'phone': '+998900112116',
            'code': '1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_verified'], True)

    def test_get_user(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], '+998900112116')

    def test_update_user(self):
        url = reverse('user-detail', args=[self.user.id])
        data = {
            'phone': '+998900112116',
            'full_name': 'Test User',
            'phone2': '+998939036903',
            'is_verified': True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_verified'], True)

    def test_delete_user(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_get_user_list(self):
        url = reverse('users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_user_with_no_data(self):
        url = reverse('user-create')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_no_phone(self):
        url = reverse('user-create')
        data = {
            'full_name': 'Test User',
            'phone2': '+998939036903',
            'is_verified': False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_no_full_name(self):
        url = reverse('user-create')
        data = {
            'phone': '+998900112116',
            'phone2': '+998939036903',
            'is_verified': False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_no_phone2(self):
        url = reverse('user-create')
        data = {
            'phone': '+998900112116',
            'full_name': 'Test User',
            'is_verified': False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user_with_no_id(self):
        url = reverse('user-detail', args=[0])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        



