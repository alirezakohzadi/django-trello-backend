from django.db import models
from cards.models import Card
from django.contrib.auth.models import User

class Comment(models.Model):
    card = models.ForeignKey(Card, verbose_name="comments", on_delete=models.CASCADE)
    auther = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[0:30]