import logging

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)
from aiohttp import web
from config.main_config import Config, load_config
from dotenv import load_dotenv
from handlers.routers import main_router
from keyboards.main_keyboards import main_menu

config: Config = load_config()
load_dotenv()

WEBHOOK_PATH = f"/bot/{config.tg_bot.token}"

WEBHOOK_URL = config.webhook.base_url + WEBHOOK_PATH


async def on_startup(bot: Bot) -> None:
    try:
        await bot.set_webhook(WEBHOOK_URL)
    except Exception as e:
        logging.error(e)


def main() -> None:
    """
    Инициализация telegram-бота.
    """

    dp: Dispatcher = Dispatcher()
    dp.startup.register(on_startup)
    dp.startup.register(main_menu)
    dp.include_router(main_router)

    bot: Bot = Bot(
        token=config.tg_bot.token
    )
    app: web.Application = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=config.webhook.secret,
    )

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(
        app,
        dp,
        bot=bot,
    )

    web.run_app(
        app=app,
        host=config.webserver.host,
        port=int(config.webserver.port),
    )


if __name__ == "__main__":
    main()
