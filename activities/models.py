from django.db import models
from django.contrib.auth.models import User
from boards.models import Board


class Activity(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    board = models.ForeignKey(
        Board,
        related_name="activities",
        on_delete=models.CASCADE
    )

    action = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]