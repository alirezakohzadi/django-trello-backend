from django.db import models
from lists.models import List




class Card(models.Model):
    list = models.ForeignKey(List, related_name="cards" ,on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
