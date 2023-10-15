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
        if self.value == enums.Round.PREFLOP.value:
            return "preflop"
        if self.value == enums.Round.FLOP.value:
            return "flop"
        if self.value == enums.Round.TURN.value:
            return "turn"
        if self.value == enums.Round.RIVER.value:
            return "river"

        return "showdown"
