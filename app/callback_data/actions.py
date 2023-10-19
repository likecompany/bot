from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class ActionsCallbackData(CallbackData, prefix="actions"):
    redis_callback_data_key: str


class ExecuteActionCallbackData(CallbackData, prefix="execute_action"):
    action: int
    amount: int
    position: int
    redis_callback_data_key: str
