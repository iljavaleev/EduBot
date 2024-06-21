from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from callbacks.callbacks_states.event_states import (
    GenericEventState,
    NotificationChoiceState,
    RepeatChoiceOrExitState,
)
from callbacks.events.event_callbacks import (
    EventNotificationChoiceCallback,
    EventRegisterFormCallback,
    EventRepeatNotificationChoiceOrExitCallback,
)
from utils.utils import get_template

template = get_template('event_templates/registration.j2')


def get_accept() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    accept = InlineKeyboardButton(
        text=template.render(button='accept'),
        callback_data=EventRegisterFormCallback(
            state=GenericEventState.yes).pack())
    decline = InlineKeyboardButton(
        text=template.render(button='decline'),
        callback_data=EventRegisterFormCallback(
            state=GenericEventState.no).pack())
    builder.row(accept, decline)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )


def create_make_bio_changes() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    button_next = InlineKeyboardButton(
        text=template.render(button='yes'),
        callback_data=EventRegisterFormCallback(
            state=GenericEventState.yes).pack())
    button_previous = InlineKeyboardButton(
        text=template.render(button='no'),
        callback_data=EventRegisterFormCallback(
            state=GenericEventState.no).pack())
    kb_builder.row(button_next, button_previous)

    return kb_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )


def create_notification_choice_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    button_now = InlineKeyboardButton(
        text=template.render(button='now'),
        callback_data=EventNotificationChoiceCallback(
            state=NotificationChoiceState.now
        ).pack())
    button_hour_before = InlineKeyboardButton(
        text=template.render(button='hour_before'),
        callback_data=EventNotificationChoiceCallback(
            state=NotificationChoiceState.hour
        ).pack())
    button_in_moment = InlineKeyboardButton(
        text=template.render(button='in_moment'),
        callback_data=EventNotificationChoiceCallback(
            state=NotificationChoiceState.moment
        ).pack())
    kb_builder.row(button_in_moment, button_hour_before)
    kb_builder.row(button_now)

    return kb_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )


def repeat_notification_choice_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    button_repeat = InlineKeyboardButton(
        text=template.render(button='repeat'),
        callback_data=EventRepeatNotificationChoiceOrExitCallback(
            state=RepeatChoiceOrExitState.repeat
        ).pack())
    button_exit = InlineKeyboardButton(
        text=template.render(button='exit'),
        callback_data=EventRepeatNotificationChoiceOrExitCallback(
            state=RepeatChoiceOrExitState.exit
        ).pack())
    kb_builder.row(button_repeat, button_exit)
    return kb_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
