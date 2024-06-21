import datetime

from celeryapp.utils import (
    delete_notification_with_task,
    get_or_update_task,
    send_article_task_construct,
)

from .models import ArticleNotification


def create_article_notification_task(
        instance: ArticleNotification,
        eta: datetime
) -> None:
    """
    Создание таска по времени в зависимости от типа.
    """
    task = get_or_update_task(instance)
    if task is None:
        return

    send_article_task_construct(
        kwargs={
            "notification_id": instance.notification_ptr_id,
        },
        task_id=task.uuid,
        eta=eta,
    )


def delete_article_notification_with_task(
        instance: ArticleNotification
) -> None:
    delete_notification_with_task(instance)
