from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from callbacks.callbacks_states.main_states import MainState
from callbacks.main_callbacks import MainCallback
from keyboards.event_keyboard.event_keyboards import (
    create_start_event_keyboard,
)
from utils.utils import get_template

from .main import router as main_router
from .registration import router as registration_router

event_router = Router()
event_router.include_routers(main_router)
event_router.include_routers(registration_router)


template = get_template('event_templates/event_templates.j2')


@event_router.callback_query(MainCallback.filter(F.state == MainState.events))
async def process_events(callback_query: CallbackQuery):
    await callback_query.message.answer(
        text=template.render(state='start'),
        reply_markup=create_start_event_keyboard(),
        parse_mode=ParseMode.MARKDOWN_V2
    )
