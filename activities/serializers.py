from rest_framework.serializers import ModelSerializer
from .models import Activity

from boards.models import Board
from boards.serializers import BoardMiniSrz
from user.serializers import UserSrz


# class BoardMiniSrz(ModelSerializer):
#     class Meta:
#         model = Board
#         fields = ["id", "title"]



class ActivitySrz(ModelSerializer):
    user = UserSrz(read_only=True)
    board = BoardMiniSrz(read_only=True)
    class Meta:
        model = Activity
        fields = "__all__"


