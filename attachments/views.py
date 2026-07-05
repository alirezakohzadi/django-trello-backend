from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Attachment
from .serializers import AttachmentSrz


class AttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = AttachmentSrz
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Attachment.objects.filter(
            card__list__board__owner=self.request.user
        )