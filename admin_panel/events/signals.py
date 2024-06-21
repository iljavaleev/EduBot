from celeryapp.utils import create_preview_task, send_event_task_construct
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import BotUserEvent, Event, EventNotification
from .utils import (
    create_before_event_notification_task,
    delete_event_notification_with_task,
)


@receiver(post_save, sender=Event)
def save_event(sender, instance: Event, **kwargs):
    """
    Если завершено создание эвента(есть ссылка, время
    и админ поставил флаг) происходит незамедлительная
    рассылка всем пользователям, которые указали 'Получить ссылку сейчас',
    но не получили(была не готова и проч).
    """
    if instance.do_broadcast:
        send_event_task_construct(
            kwargs={
                "event_id": instance.id,
                "notification_type":
                    BotUserEvent.RemindType.LINK_READY.value,
            }
        )


@receiver(post_save, sender=EventNotification)
def save_event_notification(sender,
                            instance: EventNotification,
                            **kwargs):
    """
    При создании или изменении нотификации для События проверяется тип
    и создаются таски по расписанию:
    - два таска по рассылке с напоминанием за час и в сомент начала
    - рассылка на экстренный случай(изменения и тп).
    """
    if instance.preview:
        create_preview_task(instance=instance)
    if (instance.notification_type == EventNotification.
            EventNotificationType.HOUR_BEFORE_EVENT_NOTIFICATION.value):
        create_before_event_notification_task(
            instance,
            BotUserEvent.RemindType.HOUR.value
        )
    elif (instance.notification_type
          == EventNotification.EventNotificationType
                  .IN_MOMENT_BEFORE_EVENT_NOTIFICATION.value):
        create_before_event_notification_task(
            instance,
            BotUserEvent.RemindType.IN_MOMENT.value
        )
    elif (instance.notification_type
          == EventNotification.EventNotificationType
                  .NOTIFY_IMMEDIATELY.value):
        send_event_task_construct(
            kwargs={
                "event_id": instance.event.id,
                "notification_id": instance.notification_ptr_id,
                "notification_type": None
            }
        )


@receiver(post_delete, sender=EventNotification)
def delete_event_notification(sender, instance: EventNotification, **kwargs):
    delete_event_notification_with_task(instance)
