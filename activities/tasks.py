from celery import shared_task

from .models import Activity
from boards.models import Board
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def create_activity(user_id, board_id, action):
    user = User.objects.get(id=user_id)
    board = Board.objects.get(id=board_id)

    Activity.objects.create(
        user=user,
        board=board,
        action=action
    )