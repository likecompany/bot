from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class CreateGameCallbackData(CallbackData, prefix="create_game"):
    ...
