from enum import Enum

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks.callbacks_states.question_states import FAQState
from callbacks.questions.question_callbacks import FAQCallback
from utils.utils import FaqButton, get_template

template = get_template('question_templates/faq_templates.j2')


def create_faq_keyboard(
        button_type: Enum,
        buttons: list[FaqButton] = None
) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    back_list = [
        FAQState.back_to_universities,
        FAQState.back_to_programs,
        FAQState.back_to_questions,
        FAQState.back_to_sub_questions
    ]

    if buttons is not None:
        for button in buttons:
            kb_builder.row(InlineKeyboardButton(
                text=button.text,
                callback_data=FAQCallback(
                    button_type=button_type,
                    object_id=button.object_id,
                    answer=button.answer if hasattr(button, 'answer') else None
                ).pack()
            ))
    buttons = [
        InlineKeyboardButton(
            text='<' * (button_type.value + 1),
            callback_data=FAQCallback(state=FAQState.end).pack()
        )
    ]
    for i in range(button_type.value):
        buttons.append(
            InlineKeyboardButton(
                text="<" * (button_type.value - i),
                callback_data=FAQCallback(
                    state=back_list[i]
                ).pack())
        )
    kb_builder.row(*buttons)

    return kb_builder.as_markup(one_time_keyboard=True)
