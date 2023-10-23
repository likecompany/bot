from __future__ import annotations

from typing import Optional

from aiogram.filters.callback_data import CallbackData


class PinCallbackData(CallbackData, prefix="pin"):
    value: Optional[str] = None
    erase: bool = False
    confirm: bool = False
