from rest_framework import viewsets 
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Label
from .seializers import LabelSrz
# Create your views here.




class LabelViewSet(viewsets.ModelViewSet):
    serializer_class = LabelSrz
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return Label.objects.filter(
            board__owner = self.request.user
        ).order_by("title")
    
    def perform_create(self, serializer):
        boaed = serializer.validated_data["board"]


        if boaed.owner != self.request.user:
            raise PermissionDenied("شما اجازه ساخت برچسب برای این برد را ندارید.")
        serializer.save()
    