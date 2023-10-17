from __future__ import annotations

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import (
    ActionsCallbackData,
    CardsCallbackData,
    ExitCallbackData,
    JoinCallbackData,
    PlayersCallbackData,
)


def players_game_inline_keyboard_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Join", data=JoinCallbackData().pack()),
        InlineKeyboardButton(text="Exit", data=ExitCallbackData().pack()),
    )

    return builder


def game_inline_keyboard_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Actions", data=ActionsCallbackData().pack()))
    builder.row(InlineKeyboardButton(text="Players", data=PlayersCallbackData().pack()))
    builder.row(InlineKeyboardButton(text="View Cards", callback_data=CardsCallbackData().pack()))

    return builder
