from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class UserAuthTest(APITestCase):

    def test_register_user(self):

        url = "/user/register/"

        data = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "12345678"
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )


    def test_login_user(self):

        register_url = "/user/register/"

        self.client.post(
            register_url,
            {
                "username": "testuser",
                "email": "test@test.com",
                "password": "12345678"
            }
        )


        login_url = "/user/create/token/"

        response = self.client.post(
            login_url,
            {
                "username": "testuser",
                "password": "12345678"
            }
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn(
            "access",
            response.data
        )