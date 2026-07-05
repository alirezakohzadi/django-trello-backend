from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import BoardSrz
from .models import Board
from django.db.models import Q





class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSrz
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return Board.objects.filter(
            Q(owner=self.request.user) |
            Q(members=self.request.user)
        ).distinct()
    

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        board = self.get_object()

        
        if board.owner != self.request.user:
            raise PermissionDenied("فقط مالک برد می‌تواند آن را ویرایش کند.")
        serializer.save()
