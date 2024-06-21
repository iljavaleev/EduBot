from aiogram.filters.callback_data import CallbackData


class ArticleInfoCallbackFactory(
    CallbackData,
    prefix='article_info',
):
    article_id: int
