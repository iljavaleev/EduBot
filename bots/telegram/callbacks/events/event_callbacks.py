from aiogram.filters.callback_data import CallbackData


class EventStartCallbackFactory(CallbackData, prefix='event'):
    state: str


class EventRegisterFormCallback(
    EventStartCallbackFactory,
    prefix='event_registration_form'
):
    ...


class EventNotificationChoiceCallback(
    CallbackData,
    prefix='event_notification_choice'
):
    state: int


class EventRepeatNotificationChoiceOrExitCallback(
    EventStartCallbackFactory,
    prefix='event_repeat_or_exit'
):
    ...


class EventRegistrationCallbackFactory(
    CallbackData,
    prefix='event_registration',
):
    event_id: int


class EventInfoCallbackFactory(
    CallbackData,
    prefix='event_info',
):
    event_id: int
    event_type: str | None = None
