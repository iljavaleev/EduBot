from typing import Type

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter, and_f, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, any_state, default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery
from alchemy.crud import Base
from alchemy.models import (
    Program,
    ProgramName,
    Question,
    QuestionContent,
    SubQuestion,
    SubQuestionContent,
    University,
)
from callbacks.callbacks_states.question_states import (
    ButtonState,
    FAQState,
    QuestionState,
)
from callbacks.questions.question_callbacks import (
    FAQCallback,
    QuestionCallback,
)
from handlers.main_handlers import process_menu
from keyboards.question_keyboard.faq_keyboards import create_faq_keyboard
from sqlalchemy.sql import text
from utils.utils import FaqButton, FaqQButton, get_template

template = get_template('question_templates/faq_templates.j2')
storage = MemoryStorage()
faq_router = Router()


class FAQForm(StatesGroup):
    programs = State()
    questions = State()
    sub_questions = State()
    answer = State()


@faq_router.callback_query(
    FAQCallback.filter(F.state == FAQState.end),
    StateFilter(any_state)
)
async def process_faq_out(
        callback_query: CallbackQuery,
        state: FSMContext
) -> None:
    await state.clear()
    await process_menu(callback_query.message, state=state)


@faq_router.callback_query(or_f(
    and_f(QuestionCallback.filter(F.state == QuestionState.faq),
          StateFilter(default_state)),
    and_f(FAQCallback.filter(F.state == FAQState.back_to_universities),
          ~StateFilter(default_state)))
)
async def process_faq_question_universities(
        callback_query: CallbackQuery,
        state: FSMContext
) -> None:

    universities: list[Type[University]] = await University.get_all()

    await callback_query.message.answer(
        text=template.render(state='university'),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=create_faq_keyboard(
            buttons=[FaqButton(
                u.name,
                u.id) for u in universities] if universities else None,
            button_type=ButtonState.university
        )
    )

    await state.set_state(FAQForm.programs)


@faq_router.callback_query(
    or_f(and_f(FAQCallback.filter(F.button_type == ButtonState.university),
               StateFilter(FAQForm.programs)),
         and_f(FAQCallback.filter(F.state == FAQState.back_to_programs),
               ~StateFilter(default_state)))
)
async def process_faq_question_programs(
        callback_query: CallbackQuery,
        callback_data: FAQCallback,
        state: FSMContext
) -> None:

    if callback_data.state == FAQState.back_to_programs:
        data = await state.get_data()
        university = data.get('university')
    else:
        university = callback_data.object_id
        await state.update_data(university=university)

    if university is None:
        await callback_query.message.answer(
            text=template.render(state='error'),
            parse_mode=ParseMode.MARKDOWN_V2
        )
        await state.clear()
        return
    else:
        query = f"SELECT prname.name, pr.id FROM {Program.__tablename__}" \
                f" AS pr JOIN" \
                f" {ProgramName.__tablename__} as prname" \
                f" ON pr.program_name_id=prname.id" \
                f" WHERE pr.university_id={university}"

        programs: list[Type[Program]] = await Base.get_custom_query(
            text(query)
        )

        buttons = [FaqButton(name, pk) for name, pk in programs] \
            if programs else None

        await callback_query.message.answer(
            text=template.render(state='program'),
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=create_faq_keyboard(
                buttons=buttons,
                button_type=ButtonState.program
            )
        )
        await state.set_state(FAQForm.questions)


@faq_router.callback_query(or_f(
    and_f(FAQCallback.filter(F.button_type == ButtonState.program),
          StateFilter(FAQForm.questions)),
    and_f(
        FAQCallback.filter(F.state == FAQState.back_to_questions),
        ~StateFilter(default_state)))
)
async def process_faq_question_questions(
        callback_query: CallbackQuery,
        callback_data: FAQCallback,
        state: FSMContext
) -> None:
    if callback_data.state == FAQState.back_to_questions:
        data = await state.get_data()
        program = data.get('program')
    else:
        program = callback_data.object_id
        await state.update_data(program=program)

    if program is None:
        await callback_query.message.answer(
            text=template.render(state='error'),
            parse_mode=ParseMode.MARKDOWN_V2
        )
        await state.clear()
        return
    else:
        query = f"SELECT qc.title, qc.id, qc.answer" \
                f" FROM {Question.__tablename__}" \
                f" AS q JOIN" \
                f" {QuestionContent.__tablename__} as qc" \
                f" ON q.question_id=qc.id" \
                f" WHERE q.program_id={program}"

        question_list: list[Type[Question]] = await Base.get_custom_query(
            text(query)
        )
        buttons = [FaqQButton(title, pk, answer) for
                   title,
                   pk, answer in question_list]

        await callback_query.message.answer(
            text=template.render(state='question'),
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=create_faq_keyboard(
                buttons=buttons,
                button_type=ButtonState.question
            )
        )
        await state.set_state(FAQForm.sub_questions)


@faq_router.callback_query(or_f(
    and_f(FAQCallback.filter(F.button_type == ButtonState.question),
          StateFilter(FAQForm.sub_questions)),
    and_f(
        FAQCallback.filter(F.state == FAQState.back_to_sub_questions),
        ~StateFilter(default_state)))
)
async def process_faq_sub_question_questions(
        callback_query: CallbackQuery,
        callback_data: FAQCallback,
        state: FSMContext
) -> None:
    answer = None
    if callback_data.state == FAQState.back_to_sub_questions:
        data = await state.get_data()
        question = data.get('question')
    else:
        question = callback_data.object_id
        answer = callback_data.answer
        await state.update_data(question=question)

    if question is None:
        await callback_query.message.answer(
            text=template.render(state='error'),
            parse_mode=ParseMode.MARKDOWN_V2
        )
        await state.clear()
        return
    if answer is not None:
        await callback_query.message.answer(
            text=answer,
            parse_mode=ParseMode.HTML,
            reply_markup=create_faq_keyboard(
                buttons=None,
                button_type=ButtonState.sub_question
            )
        )
    else:
        query = f"SELECT sqc.text, sqc.id FROM" \
                f" {SubQuestionContent.__tablename__}" \
                f" AS sqc JOIN" \
                f" {SubQuestion.__tablename__} as sq" \
                f" ON sqc.id=sq.content_id" \
                f" WHERE sq.question_id={question}"

        sub_question_list: list[Type[Question]] = await Base.get_custom_query(
            text(query)
        )
        buttons = [FaqButton(text, pk) for text, pk in sub_question_list]

        await callback_query.message.answer(
            text=template.render(state='sub_question'),
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=create_faq_keyboard(
                buttons=buttons,
                button_type=ButtonState.sub_question
            )
        )
        await state.set_state(FAQForm.answer)


@faq_router.callback_query(
    StateFilter(FAQForm.answer),
    FAQCallback.filter(F.button_type == ButtonState.sub_question),
)
async def process_faq_sub_question_answer(
        callback_query: CallbackQuery
) -> None:
    cb = FAQCallback().unpack(callback_query.data)
    sub_question = await SubQuestionContent.get(id=cb.object_id)

    await callback_query.message.answer(
        text=sub_question.answer,
        parse_mode=ParseMode.HTML,
        reply_markup=create_faq_keyboard(
            buttons=None,
            button_type=ButtonState.answer
        )
    )
