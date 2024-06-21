from typing import Type

from alchemy.models import BotAdmin, BotUser, BotUserEvent
from sqlalchemy import select
from utils.utils import logs


@logs
async def filter_event_users(
        event_id: int,
        notification_type: int = None
) -> list[Type[BotUser]]:
    """
    Фильтрация юзеров в зависимости от типа нотификации,
    на которые они подписались.
    """

    if notification_type is None:
        user_events: list[Type[BotUserEvent]] = \
            await BotUserEvent.get_all(event_id=event_id)
    else:
        user_events: list[Type[BotUserEvent]] = \
            await BotUserEvent.get_all(
            notification_type=notification_type,
            event_id=event_id
        )
    stmt = select(BotUser).filter(
        BotUser.id.in_((inst.user_id for inst in user_events))
    )
    return await BotUser.get_all(stmt=stmt)


@logs
async def filter_article_users() -> list[Type[BotUser]]:
    """
    Фильтрация юзеров подписанных на новости.
    """
    return await BotUser.get_all(get_articles=True)


@logs
async def filter_admin_users() -> list[Type[BotAdmin]]:
    """
    Фильтрация админов которым рассылается превью.
    """
    return await BotAdmin.get_all(get_preview=True)


@logs
async def filter_demo_day_users() -> list[Type[BotAdmin]]:
    """
    Фильтрация юзеров подписанных на демо неделю.
    """
    return await BotUser.get_all(get_demo_week=True)
