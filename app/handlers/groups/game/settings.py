from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from exc import InvalidValueError
from filters import Owner, Settings, SettingsFilter
from states import GameState

router = Router()


class SettingsCallbackData(CallbackData, prefix="settings"):
    attr: str
    text: str
    show: bool = False


def get_settings_button(attr: str, text: str, show: bool = True) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=text,
        callback_data=SettingsCallbackData(
            attr=attr,
            text=text,
            show=show,
        ).pack(),
    )


def settings_inline_keyboard_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        get_settings_button(attr="small_blind_bet", text="Small Blind"),
        get_settings_button(attr="small_blind_bet", text="Edit", show=False),
    )
    builder.row(
        get_settings_button(attr="big_blind_multiplication", text="Big Blind Multiplication"),
        get_settings_button(attr="big_blind_multiplication", text="Edit", show=False),
    )

    return builder


@router.message(
    Command(commands="settings"),
    Owner(),
)
async def settings_command_handler(message: Message) -> None:
    await message.answer(
        text="Here is your create game settings",
        reply_markup=settings_inline_keyboard_builder().as_markup(),
    )


@router.message(
    GameState.update_settings,
    Owner(),
    SettingsFilter(),
)
async def update_state_handler(
    message: Message,
    state: FSMContext,
    settings: Settings,
) -> None:
    data = await state.get_data()

    try:
        new_setting = int(message.text)
    except ValueError:
        raise InvalidValueError("Value must be integer")
    else:
        if new_setting <= 0:
            raise InvalidValueError("Value must be greater than zero")

    setattr(settings, data.pop("attr"), new_setting)
    await state.update_data(**settings.model_dump())
    await state.set_state(GameState.no_state)
    await message.answer(text="Value is updated!")


@router.callback_query(
    SettingsCallbackData.filter(),
    GameState.no_state,
    Owner(),
    SettingsFilter(),
)
async def settings_callback_query_handler(
    callback_query: CallbackQuery,
    state: FSMContext,
    callback_data: SettingsCallbackData,
    settings: Settings,
) -> None:
    if callback_data.show:
        await callback_query.answer(
            text=f"{callback_data.text}: {getattr(settings, callback_data.attr)}",
            show_alert=True,
        )
    else:
        await callback_query.message.answer(text="Enter new value")
        await state.set_state(state=GameState.update_settings)
        await state.set_data({"attr": callback_data.attr})
