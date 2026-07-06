from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend


from .serializers import CardSrz
from .models import Card
from activities.models import Activity



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


    def get_queryset(self):
        return Card.objects.filter(
            list__board__owner=self.request.user
        ).order_by("-created_at")
    




    def perform_create(self, serializer):
        list_obj = serializer.validated_data["list"]

        if list_obj.board.owner != self.request.user:
            raise PermissionDenied("شما اجازه افزودن کارت به این لیست را ندارید.")
        

        card = serializer.save()

        Activity.objects.create(
            user=self.request.user,
            board=list_obj.board,
            action=f"Created card '{card.title}'"
        )
        


    def perform_update(self, serializer):
        card = self.get_object()

        old_list = card.list

        updated_card = serializer.save()

        if old_list != updated_card.list:
            Activity.objects.create(
                user=self.request.user,
                board=updated_card.list.board,
                action=f"Moved card '{updated_card.title}'"
            )