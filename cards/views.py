from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import CardSrz
from .models import Card




class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSrz
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return Card.objects.filter(
            list__board__owner=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        list_obj = serializer.validated_data["list"]


        if list_obj.board.owner != self.request.user:
            raise PermissionDenied("شما اجازه افزودن کارت به این لیست را ندارید.")
        serializer.save()
