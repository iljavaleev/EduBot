from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from alchemy.models import Event
from callbacks.callbacks_states.event_states import StartEventState
from callbacks.events.event_callbacks import (
    EventInfoCallbackFactory,
    EventRegistrationCallbackFactory,
)
from utils.utils import get_template

template = get_template('event_templates/main.j2')


def list_events_keyboard(
        events: list[Event],
        event_type: StartEventState
) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for event in events:
        kb_button = InlineKeyboardButton(
            text=template.render(button_event=event),
            callback_data=EventInfoCallbackFactory(
                event_id=event.id,
                event_type=event_type
            ).pack(),
        )
        kb_builder.row(kb_button)

    return kb_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )


def registration_button(event: Event) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(
            text='Зарегистрироваться',
            callback_data=EventRegistrationCallbackFactory(
                event_id=event.id
            ).pack(),
        )
    )
    return kb_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
