from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend


from .models import Activity
from .serializers import ActivitySrz


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActivitySrz
    permission_classes = [IsAuthenticated]
    filterset_fields = ["board", "user"]
    ordering_fields = ["created_at"]
    search_fields = ["action"]

    def get_queryset(self):
        return Activity.objects.filter(
            board__owner=self.request.user
        )