from __future__ import annotations

from typing import Optional, Tuple

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import SettingsCallbackData
from callback_data.back import BackCallbackData
from callback_data.edit_amount import EditAmountCallbackData


def get_settings_row(
    key: str,
    attribute: str,
    text: str,
    edit_text: str = "Edit",
    chat_id: Optional[int] = None,
    message_id: Optional[int] = None,
    inline_message_id: Optional[int] = None,
) -> Tuple[InlineKeyboardButton]:
    return (
        InlineKeyboardButton(
            text=text,
            callback_data=SettingsCallbackData(
                attribute=attribute,
                text=text,
            ).pack(),
        ),
        InlineKeyboardButton(
            text=edit_text,
            callback_data=EditAmountCallbackData(
                key=key,
                attribute=attribute,
                chat_id=chat_id,
                message_id=message_id,
                inline_message_id=inline_message_id,
            ).pack(),
        ),
    )


def settings_inline_keyboard_builder(
    key: str,
    chat_id: Optional[int] = None,
    message_id: Optional[int] = None,
    inline_message_id: Optional[int] = None,
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        *get_settings_row(
            key=key,
            attribute="min_players",
            text="Min Players",
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )
    )
    builder.row(
        *get_settings_row(
            key=key,
            attribute="max_players",
            text="Max Players",
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )
    )
    builder.row(
        *get_settings_row(
            key=key,
            attribute="start_time",
            text="Start Time",
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )
    )
    builder.row(
        *get_settings_row(
            key=key,
            attribute="small_blind",
            text="Small Blind",
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )
    )
    builder.row(
        *get_settings_row(
            key=key,
            attribute="big_blind_multiplication",
            text="Big Blind Multiplication",
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )
    )
    builder.row(InlineKeyboardButton(text="Back", callback_data=BackCallbackData().pack()))

    return builder
