import time

from huey import RedisHuey
from huey.contrib.djhuey import task, db_periodic_task
from huey import crontab
from core.models import User
from django.utils import timezone
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from .models import BorrowedBook
from django.db.models import Q, ExpressionWrapper, F, DurationField

huey = RedisHuey()


@task()
def send_email(user_id, action):
    user = User.objects.get(id=user_id)
    email_map = {
        "borrowing": "You have borrowed a book",
        "returning": "You have returned a book",
        "borrowed book return date": "Your borrowed book return date is near",
        "overdue": "You have an overdue",
    }
    email_data = {
        "email_subject": action,
        "email_body": email_map[action],
        "to_email": user.email,
    }
    email = EmailMessage(
        subject=email_data["email_subject"],
        body=email_data["email_body"],
        to=[email_data["to_email"]],
        from_email=settings.EMAIL_HOST_USER,
    )
    email.send()


@db_periodic_task(crontab(minute="*"))
def notify_users():
    current_time = timezone.now()
    borrowed_books = BorrowedBook.objects.annotate(
        days=ExpressionWrapper(
            F("returned_date") - current_time, output_field=DurationField()
        )
    ).filter(days__lte=timezone.timedelta(days=3))
    for book in borrowed_books:
        send_email(book.user.id, "borrowed book return date")
