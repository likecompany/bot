from __future__ import annotations

from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import ExitCallbackData


def exit_inline_keyboard_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Exit", callback_data=ExitCallbackData().pack())

    return builder
