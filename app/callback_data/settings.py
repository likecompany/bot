from __future__ import annotations

from typing import Optional

from aiogram.filters.callback_data import CallbackData


class MySettingsCallbackData(CallbackData, prefix="edit_settings"):
    chat_id: Optional[int] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[int] = None


class SettingsCallbackData(CallbackData, prefix="settings"):
    attribute: str
    text: str
