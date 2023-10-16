from __future__ import annotations

from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import CardsCallbackData


def cards_inline_keyboard_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="View Cards", callback_data=CardsCallbackData().pack())

    return builder
