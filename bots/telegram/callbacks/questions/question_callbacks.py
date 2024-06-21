from aiogram.filters.callback_data import CallbackData


class GenericCallback(CallbackData, prefix=''):
    state: str


class QuestionCallback(GenericCallback, prefix='question'):
    ...


class CuratorCallback(GenericCallback, prefix='curator'):
    ...


class DemoWeekCallback(GenericCallback, prefix='demo_week'):
    ...


class GPTCallback(GenericCallback, prefix='gpt'):
    ...


class FAQCallback(GenericCallback, prefix='faq'):
    state: str = 'default'
    answer: str | None = None
    button_type: int = -1
    object_id: int = -1
