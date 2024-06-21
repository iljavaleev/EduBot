from aiogram.filters import BaseFilter
from aiogram.types import Message
from alchemy.models import CuratorChat


class IsReplyMessage(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        curator: CuratorChat = await CuratorChat.get(is_active=True)
        if curator is not None:
            return str(message.chat.id) == curator.chat_id \
                and message.reply_to_message is not None
