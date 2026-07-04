from rest_framework import serializers
from .models import Board
from lists.serializers import ListSrz




class BoardSrz(serializers.ModelSerializer):
    lists = ListSrz(many=True, read_only=True)
    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ["owner"]