from __future__ import annotations

from typing import Any, Dict, Union

from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject
from likeinterface import Interface
from pydantic import ValidationError

from schemas import Session


class SessionFilter(Filter):
    async def __call__(
        self,
        event: TelegramObject,
        state: FSMContext,
        interface: Interface,
    ) -> Union[bool, Dict[str, Any]]:
        try:
            return {"session": Session.model_validate(await state.get_data())}
        except ValidationError:
            return False
