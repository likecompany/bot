from __future__ import annotations

from typing import List, Optional

from aiogram.utils import markdown
from aiogram.utils.link import create_tg_link
from likeinterface import types
from pydantic import BaseModel, Field, model_validator

from utils.cards import Card, Cards


class Settings(BaseModel):
    min_players: int = Field(2, ge=2, le=6)
    max_players: int = Field(6, ge=2, le=6)
    start_time: int = Field(15, gt=0)
    small_blind: int = Field(500, gt=0)
    big_blind_multiplication: int = Field(15, gt=0)

    @model_validator(mode="after")
    def check_passwords_match(self) -> Settings:
        if self.min_players > self.max_players:
            raise ValueError("Min players can't be greater than max players")

        return self


class Player(types.Player):
    position: int
    user: types.User
    hand: List[Card] = Field(default_factory=list)

    def url(self) -> str:
        return create_tg_link(link="user", id=self.user.telegram_id)

    def mention_html(self) -> str:
        return markdown.hlink(title=self.user.full_name, url=self.url)


class Session(BaseModel):
    access: str
    game: types.Game
    cards: Cards
    actions: List[types.Action] = Field(default_factory=list)
    board: List[Card] = Field(default_factory=list)
    players: List[Player] = Field(default_factory=list)
    started: bool = False
    ready_to_start: bool = False
    start_at: Optional[float] = None
