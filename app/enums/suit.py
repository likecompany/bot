from __future__ import annotations

from enum import Enum

from likeinterface import enums


class Suit(str, Enum):
    CLUBS = enums.Suit.CLUBS.value
    DIAMONDS = enums.Suit.DIAMONDS.value
    HEARTS = enums.Suit.HEARTS.value
    SPADES = enums.Suit.SPADES.value

    def to_string_pretty(self) -> str:
        if self == Suit.CLUBS:
            return "♣"
        if self == Suit.DIAMONDS:
            return "♦️"
        if self == Suit.HEARTS:
            return "❤️"

        return "♠️"
