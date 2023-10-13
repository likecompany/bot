from __future__ import annotations

from typing import Any, Dict

from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from pydantic import BaseModel


class Settings(BaseModel):
    small_blind_bet: int = 500
    big_blind_multiplication: int = 15


class SettingsFilter(Filter):
    async def __call__(self, state: FSMContext) -> Dict[str, Any]:
        data = await state.get_data()

        return {"settings": Settings.model_validate(data)}
