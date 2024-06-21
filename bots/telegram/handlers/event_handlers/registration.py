import re

import phonenumbers
from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import CallbackQuery, Message
from alchemy.models import BotUser, BotUserEvent, Event
from callbacks.callbacks_states.event_states import (
    GenericEventState,
    NotificationChoiceState,
    RepeatChoiceOrExitState,
)
from callbacks.events.event_callbacks import (
    EventNotificationChoiceCallback,
    EventRegisterFormCallback,
    EventRegistrationCallbackFactory,
    EventRepeatNotificationChoiceOrExitCallback,
)
from handlers.main_handlers import process_menu
from keyboards.event_keyboard.registration import (
    create_make_bio_changes,
    create_notification_choice_kb,
    get_accept,
    repeat_notification_choice_kb,
)
from keyboards.main_keyboards import create_start_keyboard
from utils.utils import get_template, get_user_info


class EventRegistrationStates(StatesGroup):
    name = State()
    number = State()
    email = State()
    accept = State()
    notification_choice = State()


router = Router(name='event_handlers-registation')
template = get_template('event_templates/registration.j2')


def user_fields_exists(bot_user: BotUser) -> bool:
    return (bool(bot_user.first_name) and bool(bot_user.last_name)
            and bool(bot_user.email) and bool(bot_user.phone))


async def make_bio_changes(
        callback_query: CallbackQuery,
        state: FSMContext,
        text: str = None
) -> None:
    await state.set_state(EventRegistrationStates.name)
    if text is not None:
        await callback_query.message.answer(text=text)
    await callback_query.message.answer(text=template.render(state='0'))


def get_first_name_last_name(name: str) -> list[str] | None:
    fi = [n.strip().capitalize() for n in name.split()]
    if len(fi) != 2:
        return
    return fi


@router.callback_query(
    EventRegistrationCallbackFactory.filter()
)
async def start_registration(
    callback_query: CallbackQuery,
    callback_data: EventRegisterFormCallback,
    state: FSMContext,
):

    user_data = get_user_info(callback_query)
    bot_user = await BotUser.get(id=user_data['id'])

    if bot_user is None:
        bot_user = await BotUser.create(**user_data)
    else:
        bot_user = await bot_user.update(**user_data)
    await state.update_data(event_id=callback_data.event_id)
    await state.update_data(bot_user=bot_user)

    if user_fields_exists(bot_user):
        await callback_query.message.answer(
            text=template.render(user=bot_user),
            reply_markup=create_make_bio_changes(),
            parse_mode=ParseMode.HTML
        )
        return

    await make_bio_changes(callback_query, state)


@router.callback_query(
    StateFilter(default_state),
    EventRegisterFormCallback.filter(F.state == GenericEventState.no)
)
async def proceed_registration(callback_query: CallbackQuery,
                               state: FSMContext) -> None:
    await make_bio_changes(
        callback_query,
        state,
        text=template.render(state='decline')
    )


@router.callback_query(
    StateFilter(default_state),
    EventRegisterFormCallback.filter(F.state == GenericEventState.yes)
)
async def proceed_registration(callback_query: CallbackQuery,
                               state: FSMContext) -> None:
    await state.set_state(EventRegistrationStates.accept)
    await callback_query.message.edit_text(
        text=template.render(state='3'),
        reply_markup=get_accept()
    )


@router.message(StateFilter(EventRegistrationStates.name))
async def get_full_name(message: Message, state: FSMContext) -> None:
    fi = get_first_name_last_name(message.text)
    if fi is None:
        await state.set_state(EventRegistrationStates.name)
        await message.answer(text=template.render(state='error'))
        await message.answer(text=template.render(state='0'))
        return
    state_data = await state.get_data()
    bot_user = state_data.get('bot_user')
    bot_user.last_name, bot_user.first_name = fi
    await state.update_data(bot_user=bot_user)
    await state.set_state(EventRegistrationStates.number)
    await message.answer(text=template.render(state='1'))


@router.message(StateFilter(EventRegistrationStates.number))
async def get_number(message: Message, state: FSMContext) -> None:
    if not phonenumbers.is_valid_number(
            phonenumbers.parse(message.text, "RU")
    ):
        await state.set_state(EventRegistrationStates.number)
        await message.answer(text=template.render(state='error'))
        await message.answer(text=template.render(state='1'))
        return
    state_data = await state.get_data()
    bot_user = state_data.get('bot_user')
    bot_user.phone = message.text
    await state.update_data(bot_user=bot_user)
    await state.set_state(EventRegistrationStates.email)
    await message.answer(text=template.render(state='2'))


@router.message(StateFilter(EventRegistrationStates.email))
async def get_email(message: Message, state: FSMContext) -> None:
    """Получение почты пользователя"""
    email_valid_re = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    if not re.match(email_valid_re, message.text):
        await state.set_state(EventRegistrationStates.email)
        await message.answer(text=template.render(state='error'))
        await message.answer(text=template.render(state='2'))
        return

    state_data = await state.get_data()
    bot_user = state_data.get('bot_user')
    bot_user.email = message.text
    await state.update_data(bot_user=bot_user)
    await state.set_state(EventRegistrationStates.accept)
    await message.answer(
        text=template.render(state='3'),
        reply_markup=get_accept()
    )


@router.callback_query(
    StateFilter(EventRegistrationStates.accept),
    EventRegisterFormCallback.filter(),
)
async def process_agreement(
    callback_query: CallbackQuery,
    callback_data: EventRegisterFormCallback,
    state: FSMContext,
) -> None:
    if not callback_query.message or not isinstance(
            callback_query.message, Message
    ):
        await callback_query.answer('Не найдено сообщение')
        return

    if callback_data.state == GenericEventState.no:
        await state.clear()
        await process_menu(callback_query.message, state)
        return

    state_data = await state.get_data()
    bot_user = state_data.get('bot_user')
    await bot_user.save()

    await state.set_state(EventRegistrationStates.notification_choice)
    await callback_query.message.answer(
        text=template.render(state='4'),
        reply_markup=create_notification_choice_kb()
    )


@router.callback_query(
    StateFilter(EventRegistrationStates.notification_choice),
    EventNotificationChoiceCallback.filter()
)
async def notification_choice(
        callback: CallbackQuery,
        callback_data: EventNotificationChoiceCallback,
        state: FSMContext,
) -> None:
    state_data = await state.get_data()
    event_id = state_data.get('event_id')
    bot_user = state_data.get('bot_user')
    bot_user_event = {
        'event_id': event_id,
        'user_id': bot_user.id,
        'notification_type': callback_data.state,
    }

    event = await Event.get(id=event_id)
    if event is None:
        local_template = get_template('main_templates.j2')
        await callback.message.answer(
            text=local_template.render(state='start'),
            reply_markup=create_start_keyboard(),
        )
        await callback.answer('Произошла ошибка. Мероприятие не было найдено.')
        return
    elif (event.stream_link
          and callback_data.state == NotificationChoiceState.now):
        await callback.message.answer(
            text=template.render(event=event),
            parse_mode=ParseMode.HTML
        )
    else:
        user_event, created = await BotUserEvent.get_or_create(
            **bot_user_event
        )
        if not created:
            await callback.message.answer(
                text='Вы уже подписаны на этот тип уведомлений'
            )
        else:
            if callback_data.state == NotificationChoiceState.now:
                await callback.message.answer(
                    text=template.render(state='not_ready')
                )
            await state.update_data(user_event_id=user_event.id)

    await callback.message.answer(
        text=template.render(state='more'),
        reply_markup=repeat_notification_choice_kb()
    )


@router.callback_query(
    ~StateFilter(default_state),
    EventRepeatNotificationChoiceOrExitCallback.filter(
        F.state == RepeatChoiceOrExitState.repeat
    )
)
async def notification_choice(
        callback: CallbackQuery,
) -> None:
    await callback.message.answer(
        text=template.render(state='4'),
        reply_markup=create_notification_choice_kb()
    )


@router.callback_query(
    ~StateFilter(default_state),
    EventRepeatNotificationChoiceOrExitCallback.filter(
        F.state == RepeatChoiceOrExitState.exit
    )
)
async def notification_choice(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await state.clear()
    await process_menu(callback_query.message, state)
