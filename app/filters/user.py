from __future__ import annotations

from typing import Any, Dict, Union

from aiogram.filters import Filter
from aiogram.types import TelegramObject
from likeinterface.types import User

from schemas import Session


class UserInGame(Filter):
    async def __call__(
        self,
        event: TelegramObject,
        user: User,
        session: Session,
    ) -> Union[bool, Dict[str, Any]]:
        for position, player in enumerate(session.game.players):
            if player.id == user.id:
                return {"position": position}

        return False


class UserIsCurrent(Filter):
    async def __call__(self, event: TelegramObject, user: User, session: Session) -> bool:
        return session.game.players[session.game.current].id == user.id


class UserIsLeft(Filter):
    async def __call__(self, event: TelegramObject, user: User, session: Session) -> bool:
        for player in session.game.players:
            if player.is_left and player.id == user.id:
                return True

        return False
