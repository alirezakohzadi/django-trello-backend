from django.db import models
from boards.models import Board





class List(models.Model):
    board = models.ForeignKey(Board, related_name="lists", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)



    def __str__(self):
        return self.title