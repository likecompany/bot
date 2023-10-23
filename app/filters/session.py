from __future__ import annotations

from typing import Any, Dict, Optional, Protocol, Union

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, InlineQuery
from redis.asyncio.client import Redis

from schemas import TexasHoldemPoker


class CallbackDataProtocol(Protocol):
    redis_callback_data_key: str


class TexasHoldemPokerFilter(Filter):
    def __init__(self, join: Optional[str] = None) -> None:
        self.join = join

    async def __call__(
        self,
        event: Union[CallbackQuery, InlineQuery],
        redis: Redis,
        callback_data: Optional[CallbackDataProtocol] = None,
        args: Optional[Dict[str, Any]] = None,
    ) -> Union[bool, Dict[str, Any]]:
        if callback_data:
            redis_callback_data_key = callback_data.redis_callback_data_key
        else:
            redis_callback_data_key = args[self.join]

        if not (access := await redis.get(name=redis_callback_data_key)):
            return False

        return {
            "session": TexasHoldemPoker.model_validate_json(await redis.get(name=access)),
            "redis_callback_data_key": redis_callback_data_key,
        }
