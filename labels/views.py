from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter


from django_filters.rest_framework import DjangoFilterBackend


from .models import Label
from .seializers import LabelSrz
from activities.tasks import create_activity

class LabelViewSet(viewsets.ModelViewSet):
    serializer_class = LabelSrz
    permission_classes = [IsAuthenticated]
    search_fields = ["title"]
    filterset_fields = ["board"]


    def get_queryset(self):
        return Label.objects.filter(
            board__owner=self.request.user
        ).order_by("title")

    def perform_create(self, serializer):
        board = serializer.validated_data["board"]

        if board.owner != self.request.user:
            raise PermissionDenied(
                "شما اجازه ساخت برچسب برای این برد را ندارید."
            )

        label = serializer.save()

        create_activity.delay(
            self.request.user.id,
            label.board.id,
            f"Created label '{label.title}'"
        )


    def perform_destroy(self, instance):
        title = instance.title
        board_id = instance.board.id

        instance.delete()

        create_activity.delay(
            self.request.user.id,
            board_id,
            f"Deleted label '{title}'"
        )