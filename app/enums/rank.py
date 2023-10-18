from __future__ import annotations

from enum import Enum

from likeinterface import enums


class Rank(str, Enum):
    TWO = enums.Rank.TWO.value
    THREE = enums.Rank.THREE.value
    FOUR = enums.Rank.FOUR.value
    FIVE = enums.Rank.FIVE.value
    SIX = enums.Rank.SIX.value
    SEVEN = enums.Rank.SEVEN.value
    EIGHT = enums.Rank.EIGHT.value
    NINE = enums.Rank.NINE.value
    TEN = enums.Rank.TEN.value
    JACK = enums.Rank.JACK.value
    QUEEN = enums.Rank.QUEEN.value
    KING = enums.Rank.KING.value
    ACE = enums.Rank.ACE.value

    def to_string_pretty(self) -> str:
        if self == Rank.TWO:
            return "Two"
        if self == Rank.THREE:
            return "Three"
        if self == Rank.FOUR:
            return "Four"
        if self == Rank.FIVE:
            return "Five"
        if self == Rank.SIX:
            return "Six"
        if self == Rank.SEVEN:
            return "Seven"
        if self == Rank.EIGHT:
            return "Eight"
        if self == Rank.NINE:
            return "Nine"
        if self == Rank.TEN:
            return "Ten"
        if self == Rank.JACK:
            return "Jack"
        if self == Rank.QUEEN:
            return "Queen"
        if self == Rank.KING:
            return "King"

        return "Ace"
