from __future__ import annotations

from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import CreateGameCallbackData
from enums import Game


def create_game_inline_keyboard_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Create Texas Holdem Poker",
        callback_data=CreateGameCallbackData(game=Game.TEXAS_HOLDEM_POKER.value).pack(),
    )

    return builder
