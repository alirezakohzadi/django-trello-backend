from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from activities.tasks import create_activity
from .models import Attachment
from .serializers import AttachmentSrz
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Attachments"]
)

class AttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = AttachmentSrz
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Attachment.objects.filter(
            card__list__board__owner=self.request.user
        )

    def perform_create(self, serializer):
        card = serializer.validated_data["card"]

        if card.list.board.owner != self.request.user:
            raise PermissionDenied(
                "شما اجازه افزودن فایل به این کارت را ندارید."
            )

        attachment = serializer.save()

        create_activity.delay(
            self.request.user.id,
            card.list.board.id,
            f"Uploaded attachment to '{card.title}'"
        )

    def perform_destroy(self, instance):
        card_title = instance.card.title
        board_id = instance.card.list.board.id

        instance.delete()

        create_activity.delay(
            self.request.user.id,
            board_id,
            f"Deleted attachment from '{card_title}'"
        )