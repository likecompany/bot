from __future__ import annotations

import random
from typing import List

from likeinterface.enums import Rank, Suit
from pydantic import BaseModel


class Card(BaseModel):
    rank: Rank
    suit: Suit

    def __str__(self) -> str:
        return self.rank.value + self.suit.value


class CardsGenerator(BaseModel):
    cards: List[Card] = random.sample(
        [Card(rank=rank, suit=suit) for rank in Rank for suit in Suit], k=len(Rank) * len(Suit)
    )
    last: int = 0

    def deal(self, n: int) -> List[str]:
        cards = self.cards[self.last :]
        self.last += n

        return [str(card) for card in cards]
