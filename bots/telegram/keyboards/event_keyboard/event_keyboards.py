from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks.callbacks_states.event_states import StartEventState
from callbacks.events.event_callbacks import EventStartCallbackFactory
from utils.utils import get_template

template = get_template('event_templates/event_templates.j2')


def create_start_event_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    button_next = InlineKeyboardButton(
        text=template.render(button='next'),
        callback_data=EventStartCallbackFactory(
            state=StartEventState.next
        ).pack())
    button_previous = InlineKeyboardButton(
        text=template.render(button='previous'),
        callback_data=EventStartCallbackFactory(
            state=StartEventState.previous
        ).pack())
    kb_builder.row(button_next, button_previous)

    return kb_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
