from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from callback_data import PinCallbackData
from filters import As
from schemas import Pin
from states import PinState

router = Router()


@router.callback_query(
    PinCallbackData.filter(F.value),
    PinState.enter_pin,
    As(Pin, "pin"),
)
async def pin_value_handler(
    callback_query: CallbackQuery,
    callback_data: PinCallbackData,
    state: FSMContext,
    pin: Pin,
) -> None:
    if not pin.value and callback_data.value == "0":
        return await callback_query.answer(text="Oops, starts from 0...")

    pin.value = callback_data.value if not pin.value else pin.value + callback_data.value

    await state.update_data(pin=pin)
    return None


@router.callback_query(
    PinCallbackData.filter(F.erase),
    PinState.enter_pin,
    As(Pin, "pin"),
)
async def pin_erase_handler(
    callback_query: CallbackQuery,
    state: FSMContext,
    pin: Pin,
) -> None:
    if not pin.value:
        return await callback_query.answer(text="Nothing to erase...")

    pin.value = pin.value[:-1]

    await state.update_data(pin=pin)
    return None


@router.callback_query(
    PinCallbackData.filter(F.confirm),
    PinState.enter_pin,
    As(Pin, "pin"),
)
async def pin_confirm_handler(
    callback_query: CallbackQuery,
    state: FSMContext,
    pin: Pin,
) -> None:
    data = await state.get_data()

    if not pin.value:
        return await callback_query.answer(text="Are you sure???")

    key = data.get(pin.key)

    await state.update_data({pin.key: {**key, **{pin.attribute: pin.value}}})
    await state.set_state(state=PinState.confirm)

    await callback_query.answer(text="Okay!")
    return None
