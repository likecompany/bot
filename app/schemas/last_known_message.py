from __future__ import annotations

from typing import Optional

from aiogram.types import InlineKeyboardMarkup
from pydantic import BaseModel


class LastKnownMessage(BaseModel):
    chat_id: Optional[int] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[int] = None
    text: str
    reply_markup: InlineKeyboardMarkup
    bind_to: Optional[LastKnownMessage] = None
    state: Optional[str] = None
