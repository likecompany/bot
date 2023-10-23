from __future__ import annotations

from typing import Any, Callable, Dict, Union

from aiogram.filters import Filter
from aiogram.types import TelegramObject
from likeinterface.types import User

from schemas import Player, TexasHoldemPoker
from utils.find_if import find_if


class PlayerInGame(Filter):
    def __init__(self, condition: Callable[[Player], bool]) -> None:
        self.condition = condition

    async def __call__(
        self,
        event: TelegramObject,
        user: User,
        session: TexasHoldemPoker,
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
        session: TexasHoldemPoker,
    ) -> bool:
        return session.players[session.game.current].id == user.id
