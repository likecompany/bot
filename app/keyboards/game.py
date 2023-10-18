from __future__ import annotations

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import (
    ActionsCallbackData,
    CardsCallbackData,
    ExitCallbackData,
    JoinCallbackData,
    PlayersCallbackData,
    WinnersCallbackData,
)


def players_game_inline_keyboard_builder(redis_callback_data_key: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Join",
            data=JoinCallbackData(redis_callback_data_key=redis_callback_data_key).pack(),
        ),
        InlineKeyboardButton(
            text="Exit",
            data=ExitCallbackData(redis_callback_data_key=redis_callback_data_key).pack(),
        ),
    )

    return builder


def game_inline_keyboard_builder(redis_callback_data_key: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Actions",
            data=ActionsCallbackData(redis_callback_data_key=redis_callback_data_key).pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Players",
            data=PlayersCallbackData(redis_callback_data_key=redis_callback_data_key).pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="View Cards",
            callback_data=CardsCallbackData(
                redis_callback_data_key=redis_callback_data_key
            ).pack(),
        )
    )

    return builder


def game_ended_inline_keyboard_builder(redis_callback_data_key: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.from_markup(
        game_inline_keyboard_builder(redis_callback_data_key=redis_callback_data_key).as_markup()
        + players_game_inline_keyboard_builder(
            redis_callback_data_key=redis_callback_data_key
        ).as_markup()
    )
    builder.row(
        InlineKeyboardButton(
            text="Winners",
            data=WinnersCallbackData(redis_callback_data_key=redis_callback_data_key).pack(),
        )
    )

    return builder