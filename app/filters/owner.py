from __future__ import annotations

from typing import Optional, Union

from aiogram.enums import ChatMemberStatus
from aiogram.filters import Filter
from aiogram.types import Chat, ChatMember, TelegramObject


class Owner(Filter):
    async def __call__(
        self, event: TelegramObject, event_chat: Optional[Chat]
    ) -> Union[bool, ChatMember]:
        if not event_chat:
            return False

        for chat_member in await event_chat.get_administrators():
            if chat_member.status == ChatMemberStatus.CREATOR:
                return {"owner": chat_member}

        return False
