from django.core.cache import cache

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from activities.tasks import create_activity
from .models import Card
from .serializers import CardSrz


class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSrz
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "list",
    ]

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "created_at",
        "title",
    ]

    def clear_cache(self):
        cache.delete(f"cards_{self.request.user.id}")
        cache.delete(f"boards_{self.request.user.id}")

    def get_queryset(self):
        return Card.objects.filter(
            list__board__owner=self.request.user
        ).order_by("-created_at")

    def list(self, request, *args, **kwargs):
        cache_key = f"cards_{request.user.id}"

        data = cache.get(cache_key)

        if data is not None:
            return Response(data)

        response = super().list(request, *args, **kwargs)

        cache.set(cache_key, response.data, timeout=300)

        return response

    def perform_create(self, serializer):
        list_obj = serializer.validated_data["list"]

        if list_obj.board.owner != self.request.user:
            raise PermissionDenied(
                "شما اجازه افزودن کارت به این لیست را ندارید."
            )

        card = serializer.save()

        self.clear_cache()

        create_activity.delay(
            self.request.user.id,
            card.list.board.id,
            f"Created card '{card.title}'"
        )

    def perform_update(self, serializer):
        new_list = serializer.validated_data.get("list")

        if new_list and new_list.board.owner != self.request.user:
            raise PermissionDenied(
                "شما اجازه انتقال کارت به این لیست را ندارید."
            )

        card = self.get_object()
        old_list = card.list

        updated_card = serializer.save()

        self.clear_cache()

        if old_list != updated_card.list:
            action = f"Moved card '{updated_card.title}'"
        else:
            action = f"Updated card '{updated_card.title}'"

        create_activity.delay(
            self.request.user.id,
            updated_card.list.board.id,
            action
        )

    def perform_destroy(self, instance):
        title = instance.title
        board_id = instance.list.board.id

        instance.delete()

        self.clear_cache()

        create_activity.delay(
            self.request.user.id,
            board_id,
            f"Deleted card '{title}'"
        )