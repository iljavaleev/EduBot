from celeryapp.utils import create_preview_task
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import ArticleNotification
from .utils import (
    create_article_notification_task,
    delete_article_notification_with_task,
)


@receiver(post_save, sender=ArticleNotification)
def save_article(sender, instance: ArticleNotification, **kwargs):
    """Рассылка новостей. Происходит или сразу же после создания
    или по указанному времени."""
    if instance.preview:
        create_preview_task(instance=instance)
    elif (instance.message_time or instance.notify_immediately) and \
            instance.is_complete:
        eta = None
        if instance.message_time:
            eta = instance.message_time
        create_article_notification_task(
            instance,
            eta
        )


@receiver(post_delete, sender=ArticleNotification)
def delete_article_notification(
        sender,
        instance: ArticleNotification,
        **kwargs
):
    if instance.notify_immediately or instance.message_time:
        delete_article_notification_with_task(instance)
