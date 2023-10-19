from __future__ import annotations

from typing import Any, Dict, Optional, Protocol, Union

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, InlineQuery
from redis.asyncio.client import Redis

from schemas import Session


class CallbackDataProtocol(Protocol):
    redis_callback_data_key: str


class SessionFilter(Filter):
    async def __call__(
        self,
        event: Union[CallbackQuery, InlineQuery],
        redis: Redis,
        callback_data: Optional[CallbackDataProtocol] = None,
    ) -> Union[bool, Dict[str, Any]]:
        if callback_data:
            redis_callback_data_key = callback_data.redis_callback_data_key
        else:
            redis_callback_data_key, *_ = event.query.split()

        if not (access := await redis.get(name=redis_callback_data_key)):
            return False

        return {
            "session": Session.model_validate_json(await redis.get(name=access)),
            "redis_callback_data_key": redis_callback_data_key,
        }
