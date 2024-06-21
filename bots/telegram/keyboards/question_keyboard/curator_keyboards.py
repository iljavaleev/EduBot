from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks.callbacks_states.question_states import CuratorState
from callbacks.questions.question_callbacks import CuratorCallback
from utils.utils import get_template

template = get_template('question_templates/curator_templates.j2')


def create_another_question_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    button_yes = InlineKeyboardButton(
        text=template.render(button='yes'),
        callback_data=CuratorCallback(state=CuratorState.yes).pack()
    )
    button_no = InlineKeyboardButton(
        text=template.render(button='no'),
        callback_data=CuratorCallback(state=CuratorState.no).pack()
    )
    kb_builder.row(button_yes, button_no)
    return kb_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
