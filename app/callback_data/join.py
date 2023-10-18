from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class JoinCallbackData(CallbackData, prefix="join"):
    redis_callback_data_key: str
