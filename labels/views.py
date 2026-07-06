from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Label
from .seializers import LabelSrz
from activities.models import Activity


class LabelViewSet(viewsets.ModelViewSet):
    serializer_class = LabelSrz
    permission_classes = [IsAuthenticated]

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

        Activity.objects.create(
            user=self.request.user,
            board=board,
            action=f"Created label '{label.title}'"
        )