from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import viewsets


from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache

from activities.models import Activity
from .serializers import CardSrz
from .models import Card



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
    


    def list(self, request, *args, **kwargs):
        cache_key = f"cards_{request.user.id}"


        data = cache.get(cache_key)

        if data is not None:
            return Response(data)
    
        response =  super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=300)


        return response

    def get_queryset(self):
        return Card.objects.filter(
            list__board__owner=self.request.user
        ).order_by("-created_at")
    




    def perform_create(self, serializer):
        list_obj = serializer.validated_data["list"]

        if list_obj.board.owner != self.request.user:
            raise PermissionDenied("شما اجازه افزودن کارت به این لیست را ندارید.")
        

        card = serializer.save()
        cache.delete(f"cards_{self.request.user.id}")
        cache.delete(f"boards_{self.request.user.id}")

        Activity.objects.create(
            user=self.request.user,
            board=list_obj.board,
            action=f"Created card '{card.title}'"
        )

        

    def perform_update(self, serializer):
        new_list = serializer.validated_data.get("list")

        if new_list and new_list.board.owner != self.request.user:
            raise PermissionDenied("شما اجازه انتقال کارت به این لیست را ندارید.")

        card = self.get_object()
        old_list = card.list

        updated_card = serializer.save()

        cache.delete(f"cards_{self.request.user.id}")
        cache.delete(f"boards_{self.request.user.id}")

        if old_list != updated_card.list:
            Activity.objects.create(
                user=self.request.user,
                board=updated_card.list.board,
                action=f"Moved card '{updated_card.title}'"
            )

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete(f"cards_{self.request.user.id}")
        cache.delete(f"boards_{self.request.user.id}")