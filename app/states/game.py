from __future__ import annotations

from aiogram.fsm.state import State, StatesGroup


class GameState(StatesGroup):
    in_game = State()
