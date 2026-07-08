from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()


@shared_task(
    autoretry_for=(Exception,),
    retry_kwargs={
        "max_retries": 3,
        "countdown": 60
    }
)
def send_welcome_email(user_id):

    try:
        user = User.objects.get(id=user_id)

    except ObjectDoesNotExist:
        return "User does not exist"

    send_mail(
        subject="Welcome",
        message=f"Hello {user.username}",
        from_email="noreply@example.com",
        recipient_list=[user.email]
    )

    return "Welcome email sent"