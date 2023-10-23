from __future__ import annotations

import random
from typing import List

from pydantic import BaseModel, Field

from enums import Rank, Suit
from schemas import Card


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
