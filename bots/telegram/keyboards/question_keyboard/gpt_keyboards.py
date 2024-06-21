from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks.callbacks_states.question_states import GPTState
from callbacks.questions.question_callbacks import GPTCallback
from utils.utils import get_template

template = get_template('question_templates/gpt_templates.j2')


def create_dialog_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    button_yes = InlineKeyboardButton(text=template.render(button='yes'),
                                      callback_data=GPTCallback(
                                          state=GPTState.yes).pack())
    button_no = InlineKeyboardButton(text=template.render(button='no'),
                                     callback_data=GPTCallback(
                                         state=GPTState.no).pack())
    kb_builder.row(button_yes, button_no)

    return kb_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )


def create_continue_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    button_yes = InlineKeyboardButton(text=template.render(button='same'),
                                      callback_data=GPTCallback(
                                          state=GPTState.same).pack())
    button_no = InlineKeyboardButton(text=template.render(button='other'),
                                     callback_data=GPTCallback(
                                         state=GPTState.other).pack())
    kb_builder.row(button_yes, button_no)

    return kb_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
