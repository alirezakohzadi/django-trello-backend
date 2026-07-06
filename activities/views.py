from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Activity
from .serializers import ActivitySrz


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActivitySrz
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Activity.objects.filter(
            board__owner=self.request.user
        )