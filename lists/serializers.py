from rest_framework.serializers import ModelSerializer
from .models import List
from cards.serializers import CardSrz


class ListSrz(ModelSerializer):
    cards = CardSrz(many=True, read_only=True)

    class Meta:
        model = List
        fields = "__all__"