from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class UserTestCase(APITestCase):
    admin_login = {
        'phone_number': '0123456789',
        'password': 'randompassword',
    }
    worker_login = {
        'phone_number': '1234567890',
        'password': 'randompassword',
    }
    volunteer_login = {
        'phone_number': '2345678901',
        'password': 'randompassword',
    }

    def setUp(self):
        user_obj1 = User(phone_number='0123456789', email='test1@test.com', is_admin=True)
        user_obj1.set_password('randompassword')
        user_obj2 = User(phone_number='1234567890', email='test2@test.com', is_worker=True)
        user_obj2.set_password('randompassword')
        user_obj3 = User(phone_number='2345678901', email='test3@test.com', is_volunteer=True)
        user_obj3.set_password('randompassword')
        user_obj1.save()
        user_obj2.save()
        user_obj3.save()

    def test_user_count(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 3)

    def get_user_token(self, data):

        url = api_reverse("api-accounts:login")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data.get('token')

    # Access level for User list
    def test_al_user_list(self):
        url = api_reverse('api-accounts:user-list')
        admin_token = self.get_user_token(self.admin_login)
        worker_token = self.get_user_token(self.worker_login)
        volunteer_token = self.get_user_token(self.volunteer_login)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + admin_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + worker_token)
        response = self.client.get(url, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + volunteer_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
