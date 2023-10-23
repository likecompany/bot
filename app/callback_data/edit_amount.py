from __future__ import annotations

from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import User


class EditAmountCallbackData(CallbackData, prefix="edit_amount"):
    key: str
    attribute: str
    confirm: bool = False
    message_id: Optional[int] = None
    chat_id: Optional[int] = None
    inline_message_id: Optional[int] = None

    def job_id(self, user: User) -> str:
        return "%s%s%s%s" % (self.message_id, self.chat_id, self.inline_message_id, user.id)
