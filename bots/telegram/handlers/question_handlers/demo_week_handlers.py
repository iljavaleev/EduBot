from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from alchemy.models import BotUser
from callbacks.callbacks_states.question_states import (
    DemoWeekState,
    QuestionState,
)
from callbacks.questions.question_callbacks import (
    DemoWeekCallback,
    QuestionCallback,
)
from handlers.main_handlers import process_menu
from keyboards.question_keyboard.demo_week_keyboards import (
    create_start_demo_week_keyboard,
)
from utils.utils import get_template, get_user_info

template = get_template('question_templates/demo_week_templates.j2')
demo_week_router = Router()


@demo_week_router.callback_query(
    QuestionCallback.filter(F.state == QuestionState.demo_week)
)
async def process_curator_question(callback_query: CallbackQuery) -> None:
    await callback_query.message.answer(
        text=template.render(state='description'),
        parse_mode=ParseMode.HTML,
        reply_markup=create_start_demo_week_keyboard()
    )


@demo_week_router.callback_query(
    DemoWeekCallback.filter(F.state == DemoWeekState.yes)
)
async def process_make_subscription(
        callback_query: CallbackQuery,
        state: FSMContext
) -> None:
    user_data = get_user_info(callback_query)
    bot_user = await BotUser.get(id=user_data.get('id'))
    if bot_user is None:
        bot_user = BotUser(**user_data)
    bot_user.get_demo_week = True
    await bot_user.save()
    await callback_query.message.answer(
        text=template.render(state='subscription')
    )
    await process_menu(callback_query.message, state=state)


@demo_week_router.callback_query(
    DemoWeekCallback.filter(F.state == DemoWeekState.no)
)
async def process_make_subscription(
        callback_query: CallbackQuery,
        state: FSMContext
) -> None:
    await callback_query.message.answer(
        text=template.render(state='to_main')
    )
    await process_menu(callback_query.message, state=state)


@demo_week_router.callback_query(
    DemoWeekCallback.filter(F.state == DemoWeekState.unsubscribe)
)
async def process_make_subscription(
        callback_query: CallbackQuery,
        state: FSMContext
) -> None:
    bot_user = await BotUser.get(id=str(callback_query.from_user.id))
    if bot_user is None:
        await callback_query.message.answer(
            text=template.render(state='not_found')
        )
        return
    bot_user.get_demo_week = False
    await bot_user.save()
    await callback_query.message.answer(
        text=template.render(state='unsubscribe')
    )
    await process_menu(callback_query.message, state=state)
