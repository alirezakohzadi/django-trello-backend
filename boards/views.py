from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from django.core.cache import cache
from django.db.models import Q


from .serializers import BoardSrz
from .models import Board
from activities.tasks import create_activity

from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Bords"]
)

class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSrz
    permission_classes = [IsAuthenticated]


    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]



    search_fields = ["title"]
    ordering_fields = ["title"]





    def list(self, request, *args, **kwargs):
        cache_key = f"boards_{request.user.id}"

        data = cache.get(cache_key)

        if data is not None:
            return Response(data)

        response = super().list(request, *args, **kwargs)

        cache.set(cache_key, response.data, timeout=300)

        return response




    def get_queryset(self):
        return Board.objects.filter(
            Q(owner=self.request.user) |
            Q(members=self.request.user)
        ).distinct()
    




    def perform_create(self, serializer):
        board = serializer.save(owner=self.request.user)

        cache.delete(f"boards_{self.request.user.id}")

        create_activity.delay(
            self.request.user.id,
            board.id,
            f"Created board '{board.title}'"
        )



    def perform_update(self, serializer):
        board = self.get_object()

        if board.owner != self.request.user:
            raise PermissionDenied(
                "فقط مالک برد می‌تواند آن را ویرایش کند."
            )

        board = serializer.save()

        cache.delete(f"boards_{self.request.user.id}")

        create_activity.delay(
            self.request.user.id,
            board.id,
            f"Updated board '{board.title}'"
        )
            
    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied(
                "فقط مالک برد می‌تواند آن را حذف کند."
            )

        title = instance.title
        board_id = instance.id

        instance.delete()

        cache.delete(f"boards_{self.request.user.id}")

        create_activity.delay(
            self.request.user.id,
            board_id,
            f"Deleted board '{title}'"
        )