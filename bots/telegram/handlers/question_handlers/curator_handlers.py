from typing import Type

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import CallbackQuery, Message
from alchemy.models import CuratorAnswer, CuratorChat
from callbacks.callbacks_states.question_states import (
    CuratorState,
    QuestionState,
)
from callbacks.questions.question_callbacks import (
    CuratorCallback,
    QuestionCallback,
)
from filters.question_filters import IsReplyMessage
from handlers.main_handlers import process_menu
from keyboards.question_keyboard.curator_keyboards import (
    create_another_question_keyboard,
)
from utils.utils import get_template

curator_router = Router()
template = get_template('question_templates/curator_templates.j2')


class CuratorDialogForm(StatesGroup):
    in_dialog = State()


@curator_router.callback_query(
    QuestionCallback.filter(F.state == QuestionState.curator)
)
async def process_curator_question(
        callback_query: CallbackQuery,
        state: FSMContext
) -> None:
    await callback_query.message.answer(
        text=template.render(state='start'),
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await state.set_state(CuratorDialogForm.in_dialog)


@curator_router.message(StateFilter(default_state), IsReplyMessage())
async def process_curator_answer(message: Message) -> None:
    curator_answer: Type[CuratorAnswer] = await CuratorAnswer.get(
        id=str(message.reply_to_message.message_id)
    )
    chat_id, text = curator_answer.chat_id, curator_answer.text
    await message.bot.send_message(
        chat_id=chat_id,
        text=template.render(
            state='question',
            text_from=text[:50],
            text_to=message.text
        ),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=create_another_question_keyboard()
    )
    await CuratorAnswer.destroy(id=curator_answer.message_id)


@curator_router.message(StateFilter(CuratorDialogForm.in_dialog))
async def process_user_message(message: Message, state: FSMContext) -> None:
    curator: CuratorChat = await CuratorChat.get(is_active=True)
    bot_message = await message.bot.send_message(
        chat_id=curator.chat_id,
        text=message.text
    )
    await message.answer(
        text=template.render(state='answer_process'),
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await state.set_state(CuratorDialogForm.in_dialog)

    await CuratorAnswer.create(
        id=str(bot_message.message_id),
        chat_id=str(message.chat.id),
        text=message.text
    )
    await state.clear()


@curator_router.callback_query(
    CuratorCallback.filter(F.state == CuratorState.no)
)
async def process_not_continue(
        callback_query: CallbackQuery,
        state: FSMContext
) -> None:
    await callback_query.message.answer(
        text=template.render(state='close_dialog'),
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await process_menu(callback_query.message, state=state)


@curator_router.callback_query(
    CuratorCallback.filter(F.state == CuratorState.yes)
)
async def process_continue(
        callback_query: CallbackQuery,
        state: FSMContext
) -> None:
    await callback_query.message.answer(
        text=template.render(state='continue'),
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await state.set_state(CuratorDialogForm.in_dialog)
