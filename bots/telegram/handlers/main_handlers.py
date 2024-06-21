from aiogram import Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from keyboards.main_keyboards import create_start_keyboard
from utils.utils import get_template

template = get_template('main_templates.j2')
router: Router = Router()


@router.message(
    CommandStart(),
    StateFilter(any_state)
)
async def process_start_command(
    message: Message,
    state: FSMContext
) -> None:
    """
    Хэндлер срабатывает на команду "/start"
    и отправляет пользователю приветственное сообщение.
    """
    await message.answer_sticker(
        sticker=FSInputFile(
            path='/app/bot_static/sticker.webp'
        ),
    )
    await state.clear()
    await message.answer(
        text=template.render(state='start'),
        reply_markup=create_start_keyboard(),
        parse_mode=ParseMode.MARKDOWN_V2
    )


@router.message(Command(commands='menu'), StateFilter(any_state))
async def process_menu(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        text=template.render(state='menu'),
        reply_markup=create_start_keyboard(),
        parse_mode=ParseMode.MARKDOWN_V2
    )


@router.message(
    Command(commands='help'),
)
async def process_help_command(
    message: Message,
):
    """
    Хэндлер срабатывает на команду "/help"
    и отправляет пользователю сообщение c инструкциями по использованию бота.
    """

    await message.answer(
        text=template.render(state='help'),
        parse_mode=ParseMode.MARKDOWN_V2
    )
