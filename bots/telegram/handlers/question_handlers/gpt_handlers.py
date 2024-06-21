from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message
from callbacks.callbacks_states.question_states import GPTState, QuestionState
from callbacks.questions.question_callbacks import (
    GPTCallback,
    QuestionCallback,
)
from handlers.main_handlers import process_menu
from keyboards.question_keyboard.gpt_keyboards import (
    create_continue_keyboard,
    create_dialog_keyboard,
)
from utils.utils import get_template
from yandex_gpt.yandex_gpt import YaGPT

template = get_template('question_templates/gpt_templates.j2')

storage = MemoryStorage()
gpt_router = Router()


class GPTDialogForm(StatesGroup):
    fill_university = State()
    fill_question = State()
    continue_or_not = State()


@gpt_router.callback_query(QuestionCallback.filter(
    F.state == QuestionState.gpt)
)
async def process_gpt_question(
        callback_query: CallbackQuery,
        state: FSMContext
) -> None:
    await callback_query.message.answer(
        text=template.render(state='university_name'),
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await state.set_state(GPTDialogForm.fill_university)


@gpt_router.message(StateFilter(GPTDialogForm.fill_university))
async def process_university_name(message: Message, state: FSMContext) -> None:
    await state.update_data(university=message.text)
    await message.answer(
        text=template.render(state='question'),
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await state.set_state(GPTDialogForm.fill_question)


@gpt_router.message(StateFilter(GPTDialogForm.fill_question))
async def process_question_text(message: Message, state: FSMContext) -> None:
    await state.update_data(question=message.text)
    data: dict = await state.update_data()
    await message.answer(
        text=template.render(state='please_wait'),
        parse_mode=ParseMode.MARKDOWN_V2
    )
    answer: str = await YaGPT(
        university=data.get('university'),
        question=data.get('question')).get_answer()
    await message.answer(text=answer, parse_mode=ParseMode.HTML)

    await message.answer(
        text=template.render(state='another_question'),
        reply_markup=create_dialog_keyboard(),
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await state.set_state(GPTDialogForm.continue_or_not)


@gpt_router.callback_query(
    GPTCallback.filter(F.state == GPTState.no),
    StateFilter(GPTDialogForm.continue_or_not)
)
async def process_not_continue(
        callback_query: CallbackQuery,
        state: FSMContext
) -> None:
    await callback_query.message.answer(
        text=template.render(state='ok'),
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await state.clear()
    await process_menu(callback_query.message, state=state)


@gpt_router.callback_query(
    GPTCallback.filter(F.state == GPTState.yes),
    StateFilter(GPTDialogForm.continue_or_not)
)
async def process_continue(
        callback_query: CallbackQuery,
) -> None:
    await callback_query.message.answer(
        text=template.render(state='same_university'),
        reply_markup=create_continue_keyboard(),
        parse_mode=ParseMode.MARKDOWN_V2
    )


@gpt_router.callback_query(
    GPTCallback.filter(F.state == GPTState.same),
    StateFilter(GPTDialogForm.continue_or_not)
)
async def process_continue(
        callback_query: CallbackQuery,
        state: FSMContext
) -> None:
    await callback_query.message.answer(
        text=template.render(state='same'),
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await state.set_state(GPTDialogForm.fill_question)


@gpt_router.callback_query(
    GPTCallback.filter(F.state == GPTState.other),
    StateFilter(GPTDialogForm.continue_or_not)
)
async def process_continue(
        callback_query: CallbackQuery,
        state: FSMContext
) -> None:
    await callback_query.message.answer(
        text=template.render(state='other'),
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await state.set_state(GPTDialogForm.fill_university)
