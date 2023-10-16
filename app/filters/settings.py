from __future__ import annotations

from typing import Any, Dict

from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject

from schemas import Settings


class SettingsFilter(Filter):
    async def __call__(self, event: TelegramObject, state: FSMContext) -> Dict[str, Any]:
        return {"settings": Settings.model_validate(await state.get_data())}
