from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import viewsets

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache

from activities.tasks import create_activity
from .serializers import CardSrz
from .models import Card


class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSrz
    permission_classes = [IsAuthenticated]


    def clear_cache(self):
        cache.delete(f"cards_{self.request.user.id}")
        cache.delete(f"boards_{self.request.user.id}")


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
    


    def list(self, request, *args, **kwargs):
        cache_key = f"cards_{request.user.id}_{request.get_full_path()}"

        data = cache.get(cache_key)

        if data is not None:
            return Response(data)
    
        response =  super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=300)


        return response

    def get_queryset(self):
        return Card.objects.filter(
            Q(list__board__owner=self.request.user) |
            Q(list__board__members=self.request.user)
        ).distinct().order_by("-created_at")



    def perform_create(self, serializer):
        list_obj = serializer.validated_data["list"]

        if list_obj.board.owner != self.request.user:
            raise PermissionDenied("شما اجازه افزودن کارت به این لیست را ندارید.")
        

        card = serializer.save()
        self.clear_cache()

        create_activity.delay(
            self.request.user.id,
            card.list.board.id,
            f"Created card '{card.title}'")

    def perform_update(self, serializer):
        new_list = serializer.validated_data.get("list")

        if new_list and new_list.board.owner != self.request.user:
            raise PermissionDenied("شما اجازه انتقال کارت به این لیست را ندارید.")

        card = self.get_object()
        old_list = card.list

        updated_card = serializer.save()

        self.clear_cache()

        if old_list != updated_card.list:

            create_activity.delay(
                self.request.user.id,
                updated_card.list.board.id,
                f"Moved card '{updated_card.title}'")
        else:
            create_activity.delay(
                self.request.user.id,
                updated_card.list.board.id,
                f"Updated card '{updated_card.title}'"
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