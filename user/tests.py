from rest_framework.test import APITestCase
from rest_framework import status


class UserAuthTest(APITestCase):

    def test_register_user(self):

        response = self.client.post(
            "/user/create/",
            {
                "username": "testuser",
                "email": "test@test.com",
                "password": "12345678",
                "password2": "12345678"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )


    def test_login_user(self):

        self.client.post(
            "/user/create/",
            {
                "username": "testuser",
                "email": "test@test.com",
                "password": "12345678",
                "password2": "12345678"
            }
        )


        response = self.client.post(
            "/user/create/token/",
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


        self.assertIn(
            "refresh",
            response.data
        )