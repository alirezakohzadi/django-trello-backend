from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model


User = get_user_model()


class BoardTest(APITestCase):


    def setUp(self):

        self.user = User.objects.create_user(
            username="ali",
            password="12345678"
        )

        response = self.client.post(
            "/user/create/token/",
            {
                "username":"ali",
                "password":"12345678"
            }
        )

        token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )


    def test_create_board(self):

        response = self.client.post(
            "/boards/api/",
            {
                "title":"My Board"
            }
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )


        self.assertEqual(
            response.data["title"],
            "My Board"
        )