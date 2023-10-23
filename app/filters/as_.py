from __future__ import annotations

from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


class As(Filter, Generic[T]):
    def __init__(
        self,
        pydantic_class: Type[T],
        from_: str,
        default: Optional[T] = None,
    ) -> None:
        self.pydantic_class = pydantic_class
        self.from_ = from_
        self.default = default

    async def __call__(
        self, event: TelegramObject, state: FSMContext
    ) -> Union[bool, Dict[str, Any]]:
        data = await state.get_data()

        try:
            return {self.from_: self.pydantic_class.model_validate(data.get(self.from_, None))}
        except ValidationError:
            if self.default:
                await state.update_data({self.from_: self.default.model_dump()})
                return {self.from_: self.default}

            return False
