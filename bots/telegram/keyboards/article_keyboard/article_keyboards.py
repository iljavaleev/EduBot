from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from alchemy.models import ArticleNotification
from callbacks.article.article_callbacks import ArticleInfoCallbackFactory
from utils.utils import get_template

template = get_template('article_templates/article_templates.j2')


def create_article_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    button_subscribe = InlineKeyboardButton(
        text=template.render(button='subscribe_article'),
        callback_data=template.render(callback='subscribe_article')
    )
    button_unsubscribe = InlineKeyboardButton(
        text=template.render(button='unsubscribe_article'),
        callback_data=template.render(callback='unsubscribe_article')
    )
    button_view = InlineKeyboardButton(
        text=template.render(button='view_article'),
        callback_data=template.render(callback='view_article')
    )
    kb_builder.row(button_view)
    kb_builder.row(button_subscribe)
    kb_builder.row(button_unsubscribe)

    return kb_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )


def list_article_keyboard(
        all_articles: list[ArticleNotification]
) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for article in all_articles:
        kb_button = InlineKeyboardButton(
            text=template.render(button_article=article),
            callback_data=ArticleInfoCallbackFactory(
                article_id=article.id,
            ).pack(),
        )
        kb_builder.row(kb_button)

    return kb_builder.as_markup(
        one_time_keyboard=True
    )
