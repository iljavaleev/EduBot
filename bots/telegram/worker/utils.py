from typing import Any, Callable

import aiogram.methods as bot_methods
from aiogram.types.input_file import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from alchemy.models import Notification, NotificationContent
from utils.utils import logs

callback_dictionary: dict[str | None, Callable] = {
    None: bot_methods.SendMessage,
    "document": bot_methods.SendDocument,
    "animation": bot_methods.SendAnimation,
    "photo": bot_methods.SendPhoto,
    "video": bot_methods.SendVideo,
    "audio": bot_methods.SendAudio,
    "voice": bot_methods.SendVoice,
    "media_group": bot_methods.SendMediaGroup,
}


def construct_media(
        media: list[NotificationContent],
        caption: str = None
) -> MediaGroupBuilder:
    media_group = MediaGroupBuilder(caption=caption)
    for m in media:
        file = FSInputFile(path=f"/app/bot_media/{m.file}")
        if m.content_type == "document":
            media_group.add_document(type=m.content_type, media=file)
        elif m.content_type == "animation":
            media_group.add_video(
                type=m.content_type, media=file, has_spoiler=m.has_spoiler
            )
        elif m.content_type == "video":
            media_group.add_video(
                type=m.content_type, media=file, has_spoiler=m.has_spoiler
            )
        elif m.content_type == "photo":
            media_group.add_photo(
                type=m.content_type, media=file, has_spoiler=m.has_spoiler
            )
        elif m.content_type == "voice":
            media_group.add_audio(type=m.content_type, media=file)
        elif m.content_type == "audio":
            media_group.add_audio(type=m.content_type, media=file)
    return media_group


@logs
async def get_notification_content(notification_id: int) -> tuple[str, Any]:
    notification = await Notification.get(id=notification_id)
    media = await NotificationContent.get_all(
        notification_id=notification_id
    )
    return notification.text, media


@logs
async def send_message(bot,
                       callback: Callable,
                       chat_id: str,
                       kwargs: dict) -> None:
    await bot(callback(chat_id=int(chat_id), **kwargs))
