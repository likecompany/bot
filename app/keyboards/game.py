from __future__ import annotations

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import CardsCallbackData, PlayersCallbackData, WinnersCallbackData


def game_inline_keyboard_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Players",
            callback_data=PlayersCallbackData().pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="View Cards",
            callback_data=CardsCallbackData().pack(),
        )
    )

    return builder


def game_ended_inline_keyboard_builder() -> InlineKeyboardBuilder:
    from .exit import exit_inline_keyboard_builder

    builder = InlineKeyboardBuilder()

    builder.attach(game_inline_keyboard_builder().attach(exit_inline_keyboard_builder()))

    builder.row(
        InlineKeyboardButton(
            text="Winners",
            callback_data=WinnersCallbackData().pack(),
        )
    )

    return builder
