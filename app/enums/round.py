from __future__ import annotations

from likeinterface import enums


class Round(enums.Round):
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
