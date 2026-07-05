from rest_framework import serializers
from .models import Card

class CardSrz(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"
        read_only_fileds = ["owner"]
        