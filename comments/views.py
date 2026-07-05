from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


from .models import Comment
from .serializers import CommentSrz



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSrz
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return Comment.objects.filter(
            card__list__board__owner = self.request.user
        ).order_by("-created_at")
    
    def perform_create(self, serializer):
        card = serializer.validated_data["card"]



        if card.list.board.owner != self.request.user:
            raise PermissionDenied()
        serializer.save(auther=self.request.user)
