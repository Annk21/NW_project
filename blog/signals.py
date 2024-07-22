from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import PostCategory, Post, Category
from ..news_portal import settings
from .tasks import news_sender
import datetime

dict_message = dict()


@receiver(post_save, sender=Post)
def notify_managers_post(sender, instance, created, **kwargs):
    for category in instance.category.all():
        subscribers = [user.email for user in category.subscribed_users.all()]
        if created:
            start_word = 'Новая'
        else:
            start_word = 'Обновлена'
        subject = f'На сайте NewsPortal  {start_word.lower()} статья: {instance.title}'
        message = f'NewsPortal.\n{instance.title}:\n{instance.text[:30]}...\nПодробнее: http://127.0.0.1:8000/posts/{instance.id}'
        from_email = settings.DEFAULT_FROM_EMAIL
        news_sender.delay(subject, message, from_email, subscribers)


@receiver(m2m_changed, sender=PostCategory)
def notify_managers_posts(instance, action, pk_set, *args, **kwargs):
    if action == 'post_add':
        html_content = render_to_string(
            'post_created_email.html',
            {'post': instance, }
        )
        for pk in pk_set:
            category = Category.objects.get(pk=pk)
            subscribers = [user.email for user in category.subscribed_users.all()]

            subject = f'На сайте NewsPortal новая статья: {instance.title}'
            message = f'NewsPortal.\n{instance.title}:\n{instance.text[:30]}...\nПодробнее: http://127.0.0.1:8000/posts/{instance.id}'
            from_email = settings.DEFAULT_FROM_EMAIL
            news_sender.delay(subject, message, from_email, subscribers)
