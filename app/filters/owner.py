from __future__ import annotations

from typing import Optional

from aiogram.enums import ChatMemberStatus
from aiogram.filters import Filter
from aiogram.types import Chat, TelegramObject, User


class IsOwner(Filter):
    async def __call__(
        self, event: TelegramObject, event_from_user: Optional[User], event_chat: Optional[Chat]
    ) -> bool:
        if not event_chat:
            return False

        for chat_member in await event_chat.get_administrators():
            if (
                chat_member.status == ChatMemberStatus.CREATOR
                and chat_member.user.id == event_from_user.id
            ):
                return True

        return False
