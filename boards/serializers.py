from rest_framework import serializers
from .models import Board
from lists.serializers import ListSrz
from user.serializers import UserSrz
from django.contrib.auth.models import User

class BoardSrz(serializers.ModelSerializer):
    owner = UserSrz(read_only=True)

    members = UserSrz(
        many=True,
        read_only=True
    )

    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source="members"
    )

    lists = ListSrz(many=True, read_only=True)

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ["owner"]



class BoardMiniSrz(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id", "title"]