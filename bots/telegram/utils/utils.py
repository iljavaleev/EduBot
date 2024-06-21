import asyncio
import logging
from typing import Callable

from aiogram.types.callback_query import CallbackQuery
from jinja2 import Environment, FileSystemLoader

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")

logger = logging.getLogger(__name__)


def logs(func: Callable) -> Callable:
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as error:
            logger.error(msg=str(error))
    return wrapper


def run_loop(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(func(*args, **kwargs))
        except Exception as error:
            logger.error(msg=str(error))
        finally:
            if not loop.is_closed():
                loop.close()

    return wrapper


def get_template(path: str):
    env = Environment(loader=FileSystemLoader('templates'))
    return env.get_template(path)


def get_user_info(query: CallbackQuery) -> dict:
    user = query.from_user
    return {
        'id': str(user.id),
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'language_code': user.language_code,
    }


class FaqButton:
    def __init__(self, text, object_id):
        self.text = text
        self.object_id = object_id


class FaqQButton(FaqButton):
    def __init__(self, text, object_id, answer):
        super().__init__(text, object_id)
        self.answer = answer
