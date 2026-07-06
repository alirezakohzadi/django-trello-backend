from rest_framework.serializers import ModelSerializer
from .models import Activity


class ActivitySrz(ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"