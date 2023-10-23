from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class BackCallbackData(CallbackData, prefix="back"):
    ...
