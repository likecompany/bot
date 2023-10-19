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
            callback_data=JoinCallbackData(redis_callback_data_key=redis_callback_data_key).pack(),
        ),
        InlineKeyboardButton(
            text="Exit",
            callback_data=ExitCallbackData(redis_callback_data_key=redis_callback_data_key).pack(),
        ),
    )

    return builder


def game_inline_keyboard_builder(redis_callback_data_key: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Actions",
            callback_data=ActionsCallbackData(
                redis_callback_data_key=redis_callback_data_key
            ).pack(),
        ),
        InlineKeyboardButton(
            text="Post Action",
            switch_inline_query_current_chat=f"action {redis_callback_data_key}",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="Players",
            callback_data=PlayersCallbackData(
                redis_callback_data_key=redis_callback_data_key
            ).pack(),
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
        game_inline_keyboard_builder(redis_callback_data_key=redis_callback_data_key)
        .attach(
            players_game_inline_keyboard_builder(redis_callback_data_key=redis_callback_data_key)
        )
        .as_markup()
    )
    builder.row(
        InlineKeyboardButton(
            text="Winners",
            callback_data=WinnersCallbackData(
                redis_callback_data_key=redis_callback_data_key
            ).pack(),
        )
    )

    return builder
