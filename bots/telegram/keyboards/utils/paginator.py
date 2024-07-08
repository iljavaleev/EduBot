from typing import Any

from aiogram import F, Router, types
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Paginator:
    def __init__(
            self,
            data: Any,
            router: Router,
            model: str,
            size: int = 5,
    ):
        self.router = router
        self.size = size
        self.callback_startswith = f'{model}_page_'
        if isinstance(data, types.InlineKeyboardMarkup):
            self.list_kb = self.chunk(
                it=data.inline_keyboard,
                size=self.size
            )
        elif isinstance(data, InlineKeyboardBuilder):
            self.list_kb = self.chunk(
                it=data.export(),
                size=self.size
            )
        else:
            raise ValueError(f'{data} is not valid data')

    def __call__(
            self,
            current_page=1,
            *args,
            **kwargs
    ) -> InlineKeyboardMarkup:
        list_current_page = []
        if self.list_kb:
            list_current_page = self.list_kb[current_page]

        pagination_list = self.get_paginator(
            counts=len(self.list_kb) - 1,
            current_page=current_page,
        )

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[*list_current_page, pagination_list]
        )

        self.paginator_handler()

        return keyboard

    def get_page(self, query: CallbackQuery) -> int:
        page = query.data.split('_')[-1]
        if page == 'last':
            return len(self.list_kb) - 1
        if page == 'first':
            return 1
        return int(page)

    def chunk(self, it, size) -> list[Any]:
        parts = [it[i:i + size] for i in range(0, len(it), size)]
        return [None] + (parts if parts else [[]])

    def get_paginator(
            self,
            counts: int,
            current_page: int,
    ) -> list[InlineKeyboardButton]:
        move_to_first = InlineKeyboardButton(
            text='⏮️️',
            callback_data=f'{self.callback_startswith}first'
        )
        move_back = InlineKeyboardButton(
            text='⬅️',
            callback_data=f'{self.callback_startswith}{current_page - 1}'
        )
        center = InlineKeyboardButton(
            text=f'{current_page}/{counts}' if counts else 'Пока тут пусто',
            callback_data='pass'
        )
        move_forward = InlineKeyboardButton(
            text='➡️',
            callback_data=f'{self.callback_startswith}{current_page + 1}'
        )
        move_to_last = InlineKeyboardButton(
            text='⏭️',
            callback_data=f'{self.callback_startswith}last'
        )

        pagination_list = []

        if current_page > 1:
            pagination_list = [move_to_first, move_back]

        pagination_list.append(center)

        if counts > current_page:
            pagination_list += [move_forward, move_to_last]

        return pagination_list

    def paginator_handler(self) -> None:

        async def page_handler(query: CallbackQuery):
            page = self.get_page(query)

            await query.message.edit_reply_markup(
                reply_markup=self(current_page=page),
            )

        self.router.callback_query.register(
            page_handler,
            F.data.startswith(self.callback_startswith)
        )
