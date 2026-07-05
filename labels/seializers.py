from rest_framework.serializers import ModelSerializer
from .models import Label


class LabelSrz(ModelSerializer):
    class Meta:
        model = Label
        fields = "__all__"