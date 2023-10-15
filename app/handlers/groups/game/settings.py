from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from pydantic import ValidationError

from callback_data import SettingsCallbackData
from exc import InvalidValueError
from filters import IsOwner, SettingsFilter
from keyboards import settings_inline_keyboard_builder
from schemas import Settings
from states import GameState

router = Router()


@router.message(
    Command(commands="settings"),
    or_f(default_state, GameState.no_state),
    IsOwner(),
)
async def settings_command_handler(message: Message) -> None:
    await message.answer(
        text="Here is your create game settings",
        reply_markup=settings_inline_keyboard_builder().as_markup(),
    )


@router.message(
    GameState.update_settings,
    SettingsFilter(),
    IsOwner(),
)
async def update_state_handler(
    message: Message,
    state: FSMContext,
    settings: Settings,
) -> None:
    data = await state.get_data()

    try:
        setattr(settings, data.pop("attr"), int(message.text))
    except ValidationError:
        raise InvalidValueError("Value must be integer")

    await state.update_data(**settings.model_dump())
    await state.set_state(GameState.no_state)
    await message.answer(text="Setting is updated!")


@router.callback_query(
    SettingsCallbackData.filter(),
    GameState.no_state,
    SettingsFilter(),
    IsOwner(),
)
async def settings_callback_query_handler(
    callback_query: CallbackQuery,
    state: FSMContext,
    callback_data: SettingsCallbackData,
    settings: Settings,
) -> None:
    if callback_data.show:
        await callback_query.answer(
            text=f"{callback_data.text}: {getattr(settings, callback_data.attr)}", show_alert=True
        )
    else:
        await callback_query.message.answer(text="Enter new value")
        await state.set_state(state=GameState.update_settings)
        await state.set_data({"attr": callback_data.attr})
