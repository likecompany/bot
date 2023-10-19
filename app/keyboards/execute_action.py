from __future__ import annotations

from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import ExecuteActionCallbackData


def execute_action_inline_keyboard_builder(
    action: int,
    amount: int,
    position: int,
    redis_callback_data_key: str,
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Click to activate action",
        callback_data=ExecuteActionCallbackData(
            action=action,
            amount=amount,
            position=position,
            redis_callback_data_key=redis_callback_data_key,
        ).pack(),
    )

    return builder
