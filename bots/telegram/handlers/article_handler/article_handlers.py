from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, InaccessibleMessage
from alchemy.models import ArticleNotification, BotUser, Notification
from callbacks.article.article_callbacks import ArticleInfoCallbackFactory
from callbacks.callbacks_states.main_states import MainState
from callbacks.main_callbacks import MainCallback
from handlers.main_handlers import process_menu
from keyboards.article_keyboard.article_keyboards import (
    create_article_keyboard,
    list_article_keyboard,
)
from keyboards.utils.paginator import Paginator
from sqlalchemy import select
from utils.utils import get_template
from worker.sending import send_notification
from worker.utils import get_notification_content

router = Router()
template = get_template('article_templates/article_templates.j2')


@router.callback_query(
    MainCallback.filter(F.state == MainState.article)
)
async def process_article(callback_query: CallbackQuery) -> None:
    await callback_query.message.answer(
        text=template.render(state='article_start'),
        reply_markup=create_article_keyboard(),
        parse_mode=ParseMode.MARKDOWN_V2
    )


@router.callback_query(
    lambda c: c.data == template.render(callback='subscribe_article'),
    StateFilter(default_state)
)
async def process_subscribe(callback_query: CallbackQuery):
    user_id = str(callback_query.from_user.id)
    user, _ = await BotUser.get_or_create(id=user_id)
    if user.get_articles:
        await callback_query.message.answer(
            text=template.render(state='already_in'),
        )
        return

    user.get_articles = True
    await user.update()
    await callback_query.message.answer(
        text=template.render(state='success_in'),
    )


@router.callback_query(
    lambda c: c.data == template.render(callback='unsubscribe_article'),
    StateFilter(default_state)
)
async def process_unsubscribe(
        callback_query: CallbackQuery,
        state: FSMContext
):
    user_id = str(callback_query.from_user.id)
    user, _ = await BotUser.get_or_create(id=user_id)
    if not user.get_articles:
        await callback_query.message.answer(
            text=template.render(state='already_out'),
        )
        return
    user.get_articles = False
    await user.update()
    await callback_query.message.answer(
        text=template.render(state='success_out'),
    )
    await process_menu(callback_query.message, state=state)


@router.callback_query(
    lambda c: c.data == template.render(callback='view_article'),
    StateFilter(default_state)
)
async def process_view_article(
        callback: CallbackQuery,
) -> None:
    if not callback.message or isinstance(callback.message,
                                          InaccessibleMessage):
        await callback.answer('Не найдено сообщение')
        return

    stmt = select(ArticleNotification)\
        .join(Notification)\
        .filter(ArticleNotification.is_complete)

    articles = await ArticleNotification.get_all(stmt=stmt)
    kb = list_article_keyboard(articles)
    paginator = Paginator(kb, router=router, model='article')

    await callback.message.edit_text(
        text=template.render(state='archive'),
        reply_markup=paginator(),
    )


@router.callback_query(ArticleInfoCallbackFactory.filter())
async def process_article_info(
    callback: CallbackQuery,
    callback_data: ArticleInfoCallbackFactory,
):
    if not callback.message or isinstance(
            callback.message,
            InaccessibleMessage
    ):
        await callback.answer('Не найдено сообщение')
        return

    article = await ArticleNotification.get(id=callback_data.article_id)
    if not article:
        await callback.answer('Извините ошибка обработки данных')
        return
    users: BotUser = [BotUser(str(callback.from_user.id))]
    text, media = await get_notification_content(callback_data.article_id)

    await send_notification(users=users, text=text, media=media)
