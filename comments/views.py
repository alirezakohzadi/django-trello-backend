from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


from .models import Comment
from .serializers import CommentSrz
from activities.models import Activity

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSrz
    permission_classes = [IsAuthenticated]
    ordering_fields = ["created_at"]
    filterset_fields = ["card"]

    def get_queryset(self):
        return Comment.objects.filter(
            card__list__board__owner = self.request.user
        ).order_by("-created_at")
    
    def perform_create(self, serializer):
        card = serializer.validated_data["card"]
        Activity.objects.create(
            user=self.request.user,
            board=card.list.board,
            action="Added a comment")



        if card.list.board.owner != self.request.user:
            raise PermissionDenied()
        serializer.save(auther=self.request.user)
