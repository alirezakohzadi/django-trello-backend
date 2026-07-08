from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status


from .models import Card


User = get_user_model()




class CardModelTest(TestCase):

    def test_create_card(self):

        user = User.objects.create_user(
            username="ali",
            password="123456"
        )

        self.assertEqual(
            user.username,
            "ali"
        )







class CardAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="ali",
            password="123456"
        )


    def test_create_card_without_auth(self):

        url = "/cards/api/"

        response = self.client.post(
            url,
            {
                "title":"Docker"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )