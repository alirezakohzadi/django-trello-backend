from django.db import models
from boards.models import Board
# Create your models here.



class Label(models.Model):
    board = models.ForeignKey(Board, related_name="labels", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    color = models.CharField(max_length=30)



    def __str__(self):
        return self.title
