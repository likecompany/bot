from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject
from likeinterface import Interface
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import GetGame
from pydantic import BaseModel, Field

from utils.cards_generator import CardsGenerator


class PlayerInformation(BaseModel):
    position: int
    user_id: int
    cards: Optional[str] = None


class GameInformation(BaseModel):
    cards_generator: CardsGenerator = CardsGenerator()
    board: Optional[str] = None
    players: List[PlayerInformation] = Field(default_factory=list)


class GameFilter(Filter):
    async def __call__(
        self,
        event: TelegramObject,
        state: FSMContext,
        interface: Interface,
    ) -> Union[bool, Dict[str, Any]]:
        data = await state.get_data()

        game_access = data.get("game_access")
        try:
            game = await interface.request(method=GetGame(access=game_access))
        except LikeInterfaceError:
            return False

        return {
            "game": game,
            "game_access": game_access,
            "game_information": GameInformation.model_validate(data),
        }
