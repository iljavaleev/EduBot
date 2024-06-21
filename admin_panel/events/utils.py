import logging
from datetime import timedelta

from celeryapp.utils import (
    delete_notification_with_task,
    get_or_update_task,
    send_event_task_construct,
)

from .models import BotUserEvent, EventNotification


def create_before_event_notification_task(
        instance: EventNotification,
        _type: int
) -> None:
    """
    Создание таска по времени в зависимости от типа.
    """
    task = get_or_update_task(instance)
    if task is None:
        return
    logging.error(instance.event.title)
    eta = None
    if _type == BotUserEvent.RemindType.HOUR.value:
        eta = instance.event.date - timedelta(hours=1)
    elif _type == BotUserEvent.RemindType.IN_MOMENT:
        eta = instance.event.date - timedelta(minutes=2)

    send_event_task_construct(
        eta=eta,
        kwargs={
            "event_id": instance.event.id,
            "notification_id": instance.notification_ptr_id,
            "notification_type": _type
        },
        task_id=task.uuid,
    )


def delete_event_notification_with_task(instance: EventNotification) -> None:
    delete_notification_with_task(instance)
