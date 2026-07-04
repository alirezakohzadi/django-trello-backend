from rest_framework import serializers
from .models import Board

class BoardSrz(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id", "title"]