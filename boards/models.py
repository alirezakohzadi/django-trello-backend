from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Board(models.Model):
    owner = models.ForeignKey(User, related_name="boards", on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    members = models.ManyToManyField(User, related_name="joined_boards", blank=True)


    def __str__(self):
        return self.title