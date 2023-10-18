from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class WinnersCallbackData(CallbackData, prefix="winners"):
    redis_callback_data_key: str
