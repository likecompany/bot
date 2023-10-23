from __future__ import annotations

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import PinCallbackData
from callback_data.back import BackCallbackData


def pin_inline_keyboard_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="1", callback_data=PinCallbackData(value="1").pack()),
        InlineKeyboardButton(text="2", callback_data=PinCallbackData(value="2").pack()),
        InlineKeyboardButton(text="3", callback_data=PinCallbackData(value="3").pack()),
    )
    builder.row(
        InlineKeyboardButton(text="4", callback_data=PinCallbackData(value="4").pack()),
        InlineKeyboardButton(text="5", callback_data=PinCallbackData(value="5").pack()),
        InlineKeyboardButton(text="6", callback_data=PinCallbackData(value="6").pack()),
    )
    builder.row(
        InlineKeyboardButton(text="7", callback_data=PinCallbackData(value="7").pack()),
        InlineKeyboardButton(text="8", callback_data=PinCallbackData(value="8").pack()),
        InlineKeyboardButton(text="9", callback_data=PinCallbackData(value="9").pack()),
    )
    builder.row(
        InlineKeyboardButton(text="<", callback_data=PinCallbackData(erase=True).pack()),
        InlineKeyboardButton(text="0", callback_data=PinCallbackData(value="0").pack()),
        InlineKeyboardButton(text=">", callback_data=PinCallbackData(confirm=True).pack()),
    )
    builder.row(InlineKeyboardButton(text="Back", callback_data=BackCallbackData().pack()))

    return builder
