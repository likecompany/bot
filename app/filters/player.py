from __future__ import annotations

from typing import Any, Dict, Union

from aiogram.filters import Filter
from aiogram.types import TelegramObject
from likeinterface.types import User

from schemas import Session
from utils.find_if import find_if


class PlayerInGame(Filter):
    async def __call__(
        self,
        event: TelegramObject,
        user: User,
        session: Session,
    ) -> Union[bool, Dict[str, Any]]:
        player = find_if(
            collection=session.players, condition=lambda element: element.id == user.id
        )

        return False if not player else {"player": player}


class PlayerIsCurrent(Filter):
    async def __call__(
        self,
        event: TelegramObject,
        user: User,
        session: Session,
    ) -> bool:
        return session.players[session.game.current].id == user.id
