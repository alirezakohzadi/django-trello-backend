from rest_framework.serializers import ModelSerializer
from .models import Comment



class CommentSrz(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["auther"]