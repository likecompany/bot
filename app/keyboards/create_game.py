from __future__ import annotations

from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import CreateGameCallbackData


def create_game_inline_keyboard_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Create Game", callback_data=CreateGameCallbackData().pack())

    return builder
