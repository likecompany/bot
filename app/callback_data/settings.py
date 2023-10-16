from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class SettingsCallbackData(CallbackData, prefix="settings"):
    attr: str
    text: str
    show: bool = False
