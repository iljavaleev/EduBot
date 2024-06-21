from aiogram import F, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery
from callbacks.callbacks_states.main_states import MainState
from callbacks.main_callbacks import MainCallback
from keyboards.question_keyboard.question_keyboards import (
    create_start_questions_keyboard,
)
from utils.utils import get_template

from .curator_handlers import curator_router
from .demo_week_handlers import demo_week_router
from .faq_handlers import faq_router
from .gpt_handlers import gpt_router

router = Router()
router.include_routers(gpt_router)
router.include_routers(curator_router)
router.include_routers(faq_router)
router.include_routers(demo_week_router)

template = get_template('question_templates/question_templates.j2')


@router.callback_query(
    MainCallback.filter(F.state == MainState.question),
    StateFilter(default_state)
)
async def process_ask_question(callback_query: CallbackQuery) -> None:
    await callback_query.message.answer(
        text=template.render(state='start'),
        reply_markup=create_start_questions_keyboard(),
        parse_mode=ParseMode.MARKDOWN_V2
    )
