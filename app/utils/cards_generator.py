from __future__ import annotations

import random
from typing import List

from likeinterface.enums import Rank, Suit


class Card:
    def __init__(self, rank: Rank, suit: Suit) -> None:
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return self.rank.value + self.suit.value


class CardsGenerator:
    def __init__(self) -> None:
        self.cards = [Card(rank=rank, suit=suit) for rank in Rank for suit in Suit]
        self.last = 0

        random.shuffle(self.cards)

    def deal(self, n: int) -> List[Card]:
        cards = random.sample(self.cards[self.last :], n)
        self.last += n

        return cards  # noqa
