from __future__ import annotations

from typing import Any, Dict, Protocol, Union

from aiogram.filters import Filter
from aiogram.types import CallbackQuery
from redis.asyncio.client import Redis

from schemas import Session


class CallbackDataProtocol(Protocol):
    redis_callback_data_key: str


class SessionFilter(Filter):
    async def __call__(
        self,
        event: Union[CallbackQuery, Any],
        callback_data: CallbackDataProtocol,
        redis: Redis,
    ) -> Union[bool, Dict[str, Any]]:
        if not isinstance(event, CallbackQuery):
            return False

        if not (access := await redis.get(name=callback_data.redis_callback_data_key)):
            return False

        return {"session": Session.model_validate_json(await redis.get(name=access))}
