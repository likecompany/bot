from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import CallbackQuery, Message
from pydantic import ValidationError

from callback_data import SettingsCallbackData
from exc import InvalidValueError
from filters import SettingsFilter
from keyboards import settings_inline_keyboard_builder
from schemas import Settings

router = Router()


class SettingsState(StatesGroup):
    no_state = State()
    update = State()


@router.message(Command(commands="reset"))
async def restart(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(text="Settings have been reset")


@router.message(Command(commands="settings"))
async def settings_command_handler(message: Message) -> None:
    await message.answer(
        text="Here is your create game settings",
        reply_markup=settings_inline_keyboard_builder().as_markup(),
    )


@router.message(
    SettingsState.update,
    SettingsFilter(),
)
async def update_state_handler(
    message: Message,
    state: FSMContext,
    settings: Settings,
) -> None:
    data = await state.get_data()

    try:
        settings = settings.model_validate({data.pop("attr"): message.text, **data})
    except ValidationError:
        raise InvalidValueError("Invalid value")

    await state.update_data(**settings.model_dump())
    await state.set_state(SettingsState.no_state)
    await message.answer(text="Setting is updated!")


@router.callback_query(
    SettingsCallbackData.filter(),
    or_f(default_state, SettingsState.no_state),
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
            text=f"{callback_data.text}: {getattr(settings, callback_data.attr)}", show_alert=True
        )
    else:
        await callback_query.message.answer(text="Enter new value")
        await state.set_state(state=SettingsState.update)
        await state.set_data({"attr": callback_data.attr})
