import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class TgBot:
    token: str


@dataclass
class WebServer:
    host: str
    port: str


@dataclass
class WebHook:
    base_url: str
    path: str
    secret: str


@dataclass
class Config:
    tg_bot: TgBot
    webserver: WebServer
    webhook: WebHook


def load_config() -> Config:
    return Config(
        tg_bot=TgBot(
            token=os.getenv("BOT_TOKEN"),
        ),
        webserver=WebServer(
            host=os.getenv("WEB_SERVER_HOST"),
            port=os.getenv("WEB_SERVER_PORT"),
        ),
        webhook=WebHook(
            base_url=os.getenv("BASE_WEBHOOK_URL"),
            path=os.getenv("WEBHOOK_PATH"),
            secret=os.getenv("WEBHOOK_SECRET"),
        ),
    )
