import asyncio
from typing import Any

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types.input_file import FSInputFile
from alchemy.models import BotUser
from config.main_config import Config, load_config
from utils.utils import get_template

from .utils import callback_dictionary, construct_media, send_message

config: Config = load_config()
bot: Bot = Bot(token=config.tg_bot.token)


async def send_text_message(users: list[BotUser], text) -> None:
    """Запускается если у нас только текст."""
    callback = callback_dictionary[None]
    kwargs = {
        "text": text,
    }
    async with bot.session:
        if users:
            for user in users:
                await send_message(bot, callback, user.id, kwargs)
                await asyncio.sleep(.025)


async def send_text_with_media(users, text, file_object) -> None:
    """Запускается если у нас один файл и текст."""
    file = file_object.file
    callback = callback_dictionary[file_object.content_type]
    kwargs = {
        file_object.content_type: FSInputFile(
            path=f"/app/bot_media/{file}"
        ),
        "caption": text,
    }
    if file_object.has_spoiler:
        kwargs['has_spoiler'] = True
    async with bot.session:
        if users:
            for user in users:
                await send_message(bot, callback, user.id, kwargs)
                await asyncio.sleep(.025)


async def send_media_files(users, text, media) -> None:
    """
    Запускается, если количество media файлов 2 и более.
    Проходим по всему списку файлов и кладем,
    те что помечены флагом media group (при наличии) в список media_group.
    Сначала отправляем все файлы которые не в группе по одному.
    Если файлы группы были последним сообщением отправляем
    ее с текстом сообщения в виде caption. Если !media_group,
    то последнее сообщение просто текст нотификации.
    """

    media_group = []
    send_list = []
    for file_object in media:
        if file_object.add_to_group:
            media_group.append(file_object)
        else:
            file = file_object.file
            callback = callback_dictionary[file_object.content_type]
            kwargs = {
                file_object.content_type: FSInputFile(
                    path=f"/app/bot_media/{file}"
                ),
                "caption": None
            }
            if file_object.has_spoiler:
                kwargs['has_spoiler'] = True
            send_list.append((callback, kwargs))
    if media_group:
        callback = callback_dictionary["media_group"]
        kwargs = {"media": construct_media(media_group, text).build()}
        send_list.append((callback, kwargs))
    else:
        send_list.append((callback_dictionary[None], {'text': text}))
    async with bot.session:
        if users:
            for user in users:
                for callback, kwargs in send_list:
                    await send_message(bot, callback, user.id, kwargs)
                    await asyncio.sleep(.025)


async def send_link(users: list[BotUser], params: dict[str, Any]) -> None:
    callback = callback_dictionary[None]
    template = get_template('celery_templates/sent_event_link_template.j2')
    async with bot.session:
        if users:
            for user in users:
                if user.first_name is not None:
                    params['name'] = user.first_name
                else:
                    params['name'] = user.username

                kwargs = {
                    "text": template.render(**params),
                    "parse_mode": ParseMode.HTML
                }
                await send_message(bot, callback, user.id, kwargs)
                await asyncio.sleep(.025)


async def send_notification(
        users: list[BotUser],
        text: str,
        media: Any
) -> None:
    if not media:
        await send_text_message(users, text)
    elif len(media) == 1:
        await send_text_with_media(users, text, media[0])
    else:
        await send_media_files(users, text, media)
