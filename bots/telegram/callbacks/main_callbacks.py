from aiogram.filters.callback_data import CallbackData


class MainCallback(CallbackData, prefix='main'):
    state: str
