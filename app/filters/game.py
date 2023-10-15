from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject
from likeinterface import Interface
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import GetGame
from pydantic import BaseModel, Field

from utils.cards import Card, CardsGenerator


class PlayerInformation(BaseModel):
    position: int
    user_id: int
    cards: Optional[List[Card]] = None


class GameInformation(BaseModel):
    cards_generator: CardsGenerator = CardsGenerator()
    board: Optional[List[Card]] = None
    players: List[PlayerInformation] = Field(default_factory=list)
    ready_to_start: bool = False
    is_started: bool = False
    last_known_round: Optional[int] = None
    start_at: Optional[int] = None


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
