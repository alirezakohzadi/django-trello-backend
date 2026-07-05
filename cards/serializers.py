from rest_framework import serializers
from .models import Card
from labels.seializers import LabelSrz
class CardSrz(serializers.ModelSerializer):
    labels = LabelSrz(many=True, read_only=True)
    class Meta:
        model = Card
        fields = "__all__"
        read_only_fileds = ["owner"]
        