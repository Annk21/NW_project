from django.core.mail import send_mail
from celery import shared_task
import time


@shared_task
def news_sender(subject, message, from_email, subscribers):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        subscribers_list=subscribers,
        fail_silently=False
    )