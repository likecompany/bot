from __future__ import annotations

from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.keyboard import InlineKeyboardBuilder


def join_inline_keyboard_builder(
    bot: Bot, redis_callback_data_key: str, game: str
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Join",
        url=create_start_link(bot=bot, payload=f"game={game}&join={redis_callback_data_key}"),
    )

    return builder
