from aiogram import Bot
from aiogram.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks.callbacks_states.main_states import MainState
from callbacks.main_callbacks import MainCallback
from utils.utils import get_template

template = get_template('main_templates.j2')


async def main_menu(bot: Bot) -> None:
    main_menu_commands = [
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/start',
                   description='Начать/перезагрузить'),
        BotCommand(command='/menu',
                   description='Выход в главное меню')
    ]

    await bot.set_my_commands(main_menu_commands)


def create_start_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    button_question = InlineKeyboardButton(
        text=template.render(button='question'),
        callback_data=MainCallback(state=MainState.question).pack()
    )
    button_events = InlineKeyboardButton(
        text=template.render(button='events'),
        callback_data=MainCallback(state=MainState.events).pack()
    )
    button_news = InlineKeyboardButton(
        text=template.render(button='article'),
        callback_data=MainCallback(state=MainState.article).pack()
    )
    kb_builder.row(button_question)
    kb_builder.row(button_events)
    kb_builder.row(button_news)

    return kb_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
