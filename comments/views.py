from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from activities.tasks import create_activity
from .models import Comment
from .serializers import CommentSrz


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSrz
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_fields = [
        "card",
    ]

    ordering_fields = [
        "created_at",
    ]

    def get_queryset(self):
        return Comment.objects.filter(
            card__list__board__owner=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        card = serializer.validated_data["card"]

        if card.list.board.owner != self.request.user:
            raise PermissionDenied(
                "شما اجازه ثبت کامنت روی این کارت را ندارید."
            )

        comment = serializer.save(author=self.request.user)

        create_activity.delay(
            self.request.user.id,
            card.list.board.id,
            f"Commented on '{card.title}'"
        )

    def perform_destroy(self, instance):
        card_title = instance.card.title
        board_id = instance.card.list.board.id

        instance.delete()

        create_activity.delay(
            self.request.user.id,
            board_id,
            f"Deleted comment from '{card_title}'"
        )