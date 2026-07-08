from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model

from boards.models import Board
from lists.models import List
from .models import Card


User = get_user_model()


class CardTest(APITestCase):


    def setUp(self):

        # User اصلی
        self.user = User.objects.create_user(
            username="ali",
            password="12345678"
        )


        # گرفتن JWT Token
        token_response = self.client.post(
            "/user/create/token/",
            {
                "username": "ali",
                "password": "12345678"
            }
        )


        self.client.credentials(
            HTTP_AUTHORIZATION=
            f"Bearer {token_response.data['access']}"
        )


        # Board
        self.board = Board.objects.create(
            title="Test Board",
            owner=self.user
        )


        # List
        self.list = List.objects.create(
            title="Todo",
            board=self.board
        )


        # Card
        self.card = Card.objects.create(
            title="Old Card",
            description="old description",
            list=self.list
        )



    def test_create_card(self):

        response = self.client.post(
            "/cards/api/",
            {
                "title":"Test Card",
                "description":"testing",
                "list":self.list.id
            }
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )


        self.assertEqual(
            response.data["title"],
            "Test Card"
        )



    def test_list_cards(self):

        response = self.client.get(
            "/cards/api/"
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )



    def test_update_card(self):

        response = self.client.patch(
            f"/cards/api/{self.card.id}/",
            {
                "title":"Updated Card"
            }
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


        self.assertEqual(
            response.data["title"],
            "Updated Card"
        )



    def test_delete_card(self):

        response = self.client.delete(
            f"/cards/api/{self.card.id}/"
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )



    def test_user_cannot_access_other_board(self):

        other_user = User.objects.create_user(
            username="other",
            password="12345678"
        )


        token_response = self.client.post(
            "/user/create/token/",
            {
                "username":"other",
                "password":"12345678"
            }
        )


        self.client.credentials(
            HTTP_AUTHORIZATION=
            f"Bearer {token_response.data['access']}"
        )


        response = self.client.get(
            "/cards/api/"
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


        # نباید کارت کاربر قبلی را ببیند
        self.assertEqual(
            len(response.data["results"]),
            0
        )