from __future__ import annotations

from enum import Enum

from likeinterface import enums


class Action(Enum):
    CHECK = enums.Action.CHECK.value
    FOLD = enums.Action.FOLD.value
    CALL = enums.Action.CALL.value
    BET = enums.Action.BET.value
    RAISE = enums.Action.RAISE.value
    ALLIN = enums.Action.ALLIN.value

    def to_string(self) -> str:
        if self.value == enums.Action.CHECK.value:
            return "check"
        if self.value == enums.Action.FOLD.value:
            return "fold"
        if self.value == enums.Action.CALL.value:
            return "call"
        if self.value == enums.Action.BET.value:
            return "bet"
        if self.value == enums.Action.RAISE.value:
            return "raise"

        return "allin"

    @classmethod
    def from_string(cls, value: str) -> Action:
        if value == "check":
            return cls(Action.CHECK)
        if value == "fold":
            return cls(Action.FOLD)
        if value == "call":
            return cls(Action.CALL)
        if value == "bet":
            return cls(Action.BET)
        if value == "raise":
            return cls(Action.RAISE)

        return cls(Action.ALLIN)
