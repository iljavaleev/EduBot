from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks.callbacks_states.question_states import QuestionState
from callbacks.questions.question_callbacks import QuestionCallback
from utils.utils import get_template

template = get_template('question_templates/question_templates.j2')


def create_start_questions_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    button_faq = InlineKeyboardButton(
        text=template.render(button='FAQ'),
        callback_data=QuestionCallback(state=QuestionState.faq).pack())
    button_gpt = InlineKeyboardButton(
        text=template.render(button='GPT'),
        callback_data=QuestionCallback(state=QuestionState.gpt).pack())
    button_curator = InlineKeyboardButton(
        text=template.render(button='CURATOR'),
        callback_data=QuestionCallback(state=QuestionState.curator).pack())
    button_demo_week = InlineKeyboardButton(
        text=template.render(button='DEMO_WEEK'),
        callback_data=QuestionCallback(state=QuestionState.demo_week).pack())
    kb_builder.row(button_faq)
    kb_builder.row(button_gpt)
    kb_builder.row(button_curator)
    kb_builder.row(button_demo_week)

    return kb_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
