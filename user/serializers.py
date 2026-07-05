from rest_framework import serializers
from django.contrib.auth.models import User

from lists.serializers import ListSrz

from boards.models import Board

class UserSrz(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        ]

class UserCreateSrz(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "password", "password2", "email"]
        extra_kwargs = {"password": {"write_only" : True}}




    def validate(self, data):

        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password": "password2 is not match with password1"})
        return data    






    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user
    
    

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


class UserLoginSrz(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()