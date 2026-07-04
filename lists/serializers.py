from rest_framework.serializers import ModelSerializer
from .models import List


class ListSrz(ModelSerializer):
    class Meta:
        model = List
        fields = "__all__"