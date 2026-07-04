from rest_framework import serializers
from django.contrib.auth.models import User



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