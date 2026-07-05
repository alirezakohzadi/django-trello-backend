from rest_framework.serializers import ModelSerializer
from .models import Attachment


class AttachmentSrz(ModelSerializer):
    class Meta:
        model = Attachment
        fields = "__all__"