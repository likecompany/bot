from __future__ import annotations

from typing import Tuple

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import SettingsCallbackData


def get_settings_row(attr: str, text: str, edit_text: str = "edit") -> Tuple[InlineKeyboardButton]:
    return (
        InlineKeyboardButton(
            text=text,
            callback_data=SettingsCallbackData(
                attr=attr,
                text=text,
                show=True,
            ).pack(),
        ),
        InlineKeyboardButton(
            text=text,
            callback_data=SettingsCallbackData(
                attr=attr,
                text=edit_text,
                show=False,
            ).pack(),
        ),
    )


def settings_inline_keyboard_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(*get_settings_row(attr="min_players", text="Min Players"))
    builder.row(*get_settings_row(attr="max_players", text="Max Players"))
    builder.row(*get_settings_row(attr="start_time", text="Start Time"))
    builder.row(*get_settings_row(attr="small_blind", text="Small Blind"))
    builder.row(
        *get_settings_row(attr="big_blind_multiplication", text="Big Blind Multiplication")
    )

    return builder
