from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


User = get_user_model()

class EarthQuake(APITestCase):
    def setUp(self):
        pass