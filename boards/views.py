from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import BoardSrz
from .models import Board

class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = [BoardSrz]
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)
    

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

