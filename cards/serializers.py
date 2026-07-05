from rest_framework import serializers
from .models import Card
from labels.seializers import LabelSrz
from attachments.serializers import AttachmentSrz




class CardSrz(serializers.ModelSerializer):
    attachments = AttachmentSrz(many=True, read_only=True)
    labels = LabelSrz(many=True, read_only=True)
    class Meta:
        model = Card
        fields = "__all__"
        read_only_fileds = ["owner"]
        