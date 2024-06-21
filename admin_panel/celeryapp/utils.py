import logging
from typing import Type

from celery.app.control import Control
from celery.utils import gen_unique_id
from django.core.exceptions import ObjectDoesNotExist
from notifications.models import Notification

from admin_panel.celery_config import app

from .models import Task

BEFORE_EVENT_TASK_NAME = 'worker.celery.send_event_message'
PREVIEW_TASK_NAME = 'worker.celery.send_to_admin'
SEND_NEWS_TASK_NAME = 'worker.celery.send_article_message'
QUEUE_NAME = 'tasks'

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")

logger = logging.getLogger(__name__)


def send_event_task_construct(**kwargs) -> None:
    """
    Вспомогательная функция с аргументами по умолчанию.
    """
    return app.send_task(
        name=BEFORE_EVENT_TASK_NAME,
        queue=QUEUE_NAME,
        **kwargs
    )


def send_article_task_construct(**kwargs) -> None:
    return app.send_task(
        name=SEND_NEWS_TASK_NAME,
        queue=QUEUE_NAME,
        **kwargs
    )


def send_to_admin_task(**kwargs) -> None:
    return app.send_task(
        name=PREVIEW_TASK_NAME,
        queue=QUEUE_NAME,
        **kwargs
    )


def get_or_update_task(
        instance: Type[Notification],
) -> Type[Task] | None:
    """
    Проверяется висит ли уже таск к этой нотификации. Если да,
    то отзывается и заводится новый. Возможно изменилось время рассылки
    или тип нотификации.
    """
    task = Task.objects.filter(
        notification_id=instance.notification_ptr_id
    ).first()
    if task is None:
        task = Task.objects.create(
            notification_id=instance.notification_ptr_id,
            uuid=gen_unique_id(),
        )
    else:
        Control(app=app).revoke(
            task.uuid,
            terminate=True, signal='SIGKILL')

        task.uuid = gen_unique_id()
        task.save()
        task.refresh_from_db()

    return task


def delete_notification_with_task(instance: Type[Notification]) -> None:
    try:
        task = Task.objects.get(
            notification_id=instance.notification_ptr_id
        )
    except ObjectDoesNotExist as error:
        logger.error(msg=str(error))
        return

    Control(app=app).revoke(
        task.uuid,
        terminate=True, signal='SIGKILL')
    task.delete()


def create_preview_task(
        instance: Type[Notification]
) -> None:
    send_to_admin_task(
        kwargs={
            "notification_id": instance.notification_ptr_id,
        },
    )
