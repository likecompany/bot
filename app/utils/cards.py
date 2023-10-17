from __future__ import annotations

import random
from typing import List

from likeinterface.enums import Rank, State, Suit
from pydantic import BaseModel, Field


def suit_to_pretty_string(suit: Suit) -> str:
    if suit == Suit.CLUBS:
        return "♣"
    if suit == Suit.DIAMONDS:
        return "♦️"
    if suit == suit.HEARTS:
        return "❤️"

    return "♠️"


class Card(BaseModel):
    rank: Rank
    suit: Suit

    def as_string_pretty(self) -> None:
        return self.rank.value + suit_to_pretty_string(suit=self.suit)

    def __str__(self) -> str:
        return self.rank.value + self.suit.value


class Cards(BaseModel):
    cards: List[Card] = Field(default_factory=list)
    last: int = 0

    def deal(self, n: int) -> List[Card]:
        if not self.cards:
            self.cards = random.sample(
                [Card(rank=rank, suit=suit) for rank in Rank for suit in Suit],
                k=len(Rank) * len(Suit),
            )

        cards = self.cards[self.last : self.last + n]
        self.last += n

        return cards  # noqa: RET504

    def reset(self) -> None:
        self.last = 0
