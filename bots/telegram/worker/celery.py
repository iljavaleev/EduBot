from celery import Celery
from config.main_config import Config, load_config
from kombu import Exchange, Queue

from .for_celery_functions import (
    before_event_notification,
    send_article_notification,
    send_demo_day_notification,
    send_link_ready_message,
    send_to_admin_chat,
)

config: Config = load_config()

app = Celery("tasks")
app.conf.broker_url = "amqp://guest:guest@rabbitmq:5672/"
app.conf.imports = ('worker.celery', )
app.conf.task_queues = {
    Queue('tasks', Exchange('tasks'), routing_key='tasks'),
    Queue('demo_week', Exchange('demo_week'), routing_key='demo_week')
}
app.conf.task_acks_late = True
app.conf.task_default_priority = 5
app.conf.worker_prefetch_multiplier = 1
app.conf.worker_concurrency = 1
app.conf.timezone = 'Europe/Moscow'


@app.task(queue='tasks')
def send_event_message(
        event_id: int,
        notification_id: int | None = None,
        notification_type: int | None = None,
) -> None:
    """
    В зависимости от типа запускает ту или иную логику.
    """
    if notification_id is None:
        send_link_ready_message(event_id, notification_type)
    else:
        before_event_notification(
            event_id=event_id,
            notification_id=notification_id,
            notification_type=notification_type
        )


@app.task(queue='tasks')
def send_to_admin(notification_id: int) -> None:
    send_to_admin_chat(notification_id)


@app.task(queue='tasks')
def send_article_message(notification_id: int) -> None:
    send_article_notification(notification_id)


@app.task(queue='demo_week')
def send_demo_day(day: int) -> None:
    send_demo_day_notification(day)
