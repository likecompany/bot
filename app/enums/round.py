from __future__ import annotations

from enum import Enum

from likeinterface import enums


class Round(Enum):
    PREFLOP = enums.Round.PREFLOP.value
    FLOP = enums.Round.FLOP.value
    TURN = enums.Round.TURN.value
    RIVER = enums.Round.RIVER.value
    SHOWDOWN = enums.Round.SHOWDOWN.value

    def to_string(self) -> str:
        if self == Round.PREFLOP:
            return "preflop"
        if self == Round.FLOP:
            return "flop"
        if self == Round.TURN:
            return "turn"
        if self == Round.RIVER:
            return "river"

        return "showdown"
