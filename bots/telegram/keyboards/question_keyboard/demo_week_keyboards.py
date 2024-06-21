from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks.callbacks_states.question_states import DemoWeekState
from callbacks.questions.question_callbacks import DemoWeekCallback
from utils.utils import get_template

template = get_template('question_templates/demo_week_templates.j2')


def create_start_demo_week_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    button_yes = InlineKeyboardButton(
        text=template.render(button='yes'),
        callback_data=DemoWeekCallback(state=DemoWeekState.yes).pack()
    )
    button_no = InlineKeyboardButton(
        text=template.render(button='no'),
        callback_data=DemoWeekCallback(state=DemoWeekState.no).pack()
    )
    button_unsubscribe = InlineKeyboardButton(
        text=template.render(button='unsubscribe'),
        callback_data=DemoWeekCallback(state=DemoWeekState.unsubscribe).pack()
    )

    kb_builder.row(button_yes, button_no)
    kb_builder.row(button_unsubscribe)
    return kb_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
