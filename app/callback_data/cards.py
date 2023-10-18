from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class CardsCallbackData(CallbackData, prefix="cards"):
    redis_callback_data_key: str
