from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from likeinterface import types
from pydantic import BaseModel, Field

from utils.cards import Cards

if TYPE_CHECKING:
    from .card import Card
    from .player import Player


class PlayerActions(BaseModel):
    action: types.Action


class ActionsMixin(BaseModel):
    last_actions: List[PlayerActions] = Field(default_factory=list)
    actions: List[types.Action] = Field(default_factory=list)
    action_time: Optional[float] = None


class CardsMixin(BaseModel):
    cards: Cards
    board: List[Card] = Field(default_factory=list)


class StartMixin(BaseModel):
    started: bool = False
    ready_to_start: bool = False
    start_at: Optional[float] = None


class RoundMixin(BaseModel):
    last_round: Optional[int] = None


class TexasHoldemPoker(ActionsMixin, CardsMixin, StartMixin, RoundMixin):
    access: str
    game: Optional[types.Game] = None
    players: List[Player] = Field(default_factory=list)
    winners: Optional[str] = None
