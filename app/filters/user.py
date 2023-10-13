from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Union

from aiogram.filters import Filter
from aiogram.types import TelegramObject
from likeinterface.types import Game, User

if TYPE_CHECKING:
    from .game import GameInformation


class UserInGame(Filter):
    async def __call__(
        self,
        event: TelegramObject,
        user: User,
        game_information: GameInformation,
    ) -> Union[bool, Dict[str, Any]]:
        for player in game_information.players:
            if player.user_id == user.id:
                return {"player": player}

        return False


class UserIsCurrent(Filter):
    async def __call__(self, event: TelegramObject, user: User, game: Game) -> bool:
        return game[game.current].id == user.id


class UserIsLeft(Filter):
    async def __call__(
        self, event: TelegramObject, user: User, game_information: GameInformation
    ) -> bool:
        for player in game_information.players:
            if player.user_id == user.id:
                return False

        return True
