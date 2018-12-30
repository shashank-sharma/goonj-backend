from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status


User = get_user_model()


class UserTestCase(APITestCase):
    def setUp(self):
        user_obj = User(phone_number='0123456789', email='test@test.com')
        user_obj.set_password('randompassword')
        user_obj.save()

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_get_list(self):
        data = {}
        url = api_reverse("api-accounts:user-list")
        response = self.client.request(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_ownership(self):
        data = {
            'phone_number': '1234567890',
            'password': 'randompassword',
            'is_admin': True,
        }
        url = api_reverse("api-accounts:login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data.get('token')
        if token is not None:
            data = {}
            url = api_reverse('api-accounts:user-list')
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
            response = self.client.request(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

