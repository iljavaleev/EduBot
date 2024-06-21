from datetime import datetime
from typing import Any

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InaccessibleMessage
from alchemy.models import Event
from callbacks.callbacks_states.event_states import StartEventState
from callbacks.events.event_callbacks import (
    EventInfoCallbackFactory,
    EventRegistrationCallbackFactory,
    EventStartCallbackFactory,
)
from keyboards.event_keyboard.main import (
    list_events_keyboard,
    registration_button,
)
from keyboards.utils.paginator import Paginator
from sqlalchemy import and_, select
from utils.utils import get_template

router = Router(name='event_handlers-main')
template = get_template('event_templates/main.j2')


async def list_events(
        callback: CallbackQuery,
        stmt: Any,
        event_type: StartEventState
) -> None:
    if not callback.message or isinstance(callback.message,
                                          InaccessibleMessage):
        await callback.answer('Не найдено сообщение')
        return

    events = await Event.get_all(stmt=stmt)
    if event_type == StartEventState.next:
        text = template.render(event_list_next=True)
    else:
        text = template.render(event_list_past=True)
    kb = list_events_keyboard(events, event_type=event_type)
    paginator = Paginator(kb, router=router, model='events')

    await callback.message.edit_text(
        text=text,
        reply_markup=paginator(),
        parse_mode=ParseMode.MARKDOWN_V2
    )


@router.callback_query(
    EventStartCallbackFactory.filter(F.state == StartEventState.next)
)
async def list_active_events(
        callback: CallbackQuery,
        callback_data: EventStartCallbackFactory
):
    now = datetime.now()
    stmt = select(Event).filter(and_(
        Event.is_complete,
        Event.date > now))
    await list_events(callback, stmt, event_type=callback_data.state)


@router.callback_query(
    EventStartCallbackFactory.filter(F.state == StartEventState.previous)
)
async def list_previous_events(
        callback: CallbackQuery,
        callback_data: EventStartCallbackFactory
):
    now = datetime.now()
    stmt = select(Event).filter(and_(
        Event.is_complete,
        Event.date <= now))
    await list_events(callback, stmt, event_type=callback_data.state)


@router.callback_query(EventInfoCallbackFactory.filter())
async def process_event_info(
    callback: CallbackQuery,
    callback_data: EventRegistrationCallbackFactory,
):
    if not callback.message or isinstance(
            callback.message,
            InaccessibleMessage
    ):
        await callback.answer('Не найдено сообщение')
        return

    event = await Event.get(id=callback_data.event_id)
    if not event:
        await callback.answer('Такого мероприятия уже не существует')
        return

    if callback_data.event_type == StartEventState.next:
        await callback.message.answer(
            text=template.render(event_next=event),
            reply_markup=registration_button(event),
            parse_mode=ParseMode.HTML
        )
    else:
        await callback.message.answer(
            text=template.render(event_previous=event),
            parse_mode=ParseMode.HTML
        )
