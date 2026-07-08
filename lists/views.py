from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import List
from .serializers import ListSrz
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Lists"]
)

class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListSrz
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return List.objects.filter(board__owner=self.request.user)