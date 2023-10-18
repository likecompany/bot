from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class PlayersCallbackData(CallbackData, prefix="players"):
    redis_callback_data_key: str
