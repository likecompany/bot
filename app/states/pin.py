from __future__ import annotations

from aiogram.fsm.state import State, StatesGroup


class PinState(StatesGroup):
    enter_pin = State()
    confirm = State()
    confirmed = State()
