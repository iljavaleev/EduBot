from alchemy.models import BotUser, DemoWeek, Event
from utils.utils import logger, run_loop

from .filters import (
    filter_admin_users,
    filter_article_users,
    filter_demo_day_users,
    filter_event_users,
)
from .sending import send_link, send_notification
from .utils import get_notification_content


@run_loop
async def send_link_ready_message(
        event_id: int,
        notification_type: int
) -> None:
    users: list[BotUser] = await filter_event_users(
        event_id, notification_type
    )
    event = await Event.get(id=event_id)
    event_date, event_time = event.date.date(), event.date.time()
    params = {
        'title': event.title,
        'link': event.stream_link,
        'date': (f'{event_date.day}/'
                 f'{event_date.month}/{event_date.year}'),
        'time': f'{event_time.hour}:{event_time.minute}'
    }
    await send_link(users, params)


@run_loop
async def before_event_notification(
        event_id: int,
        notification_type: int,
        notification_id: int | None = None,
) -> None:
    users: list[BotUser] = await filter_event_users(
        event_id, notification_type
    )
    text, media = await get_notification_content(
        notification_id=notification_id
    )
    await send_notification(users=users, text=text, media=media)


@run_loop
async def send_demo_day_notification(
        week_day: int
) -> None:
    day: DemoWeek = await DemoWeek.get(weekday=week_day)
    text, media = await get_notification_content(
        notification_id=day.id
    )
    users = await filter_demo_day_users()
    if week_day == 0:
        users = [await user.update(get_demo_week=False) for user in users]
    await send_notification(users=users, text=text, media=media)


@run_loop
async def send_article_notification(notification_id: int) -> None:
    users = await filter_article_users()
    text, media = await get_notification_content(notification_id)
    await send_notification(users=users, text=text, media=media)


@run_loop
async def send_to_admin_chat(notification_id: int) -> None:
    admins = await filter_admin_users()
    text, media = await get_notification_content(notification_id)
    if not admins:
        logger.error('You must create bot admin instance with CHAT_ID first')
    else:
        await send_notification(
            users=admins,
            text=text,
            media=media
        )
