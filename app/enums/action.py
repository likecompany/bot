from __future__ import annotations

from likeinterface import enums


class Action(enums.Action):
    def to_string(self) -> str:
        if self == Action.CHECK:
            return "check"
        if self == Action.FOLD:
            return "fold"
        if self == Action.CALL:
            return "call"
        if self == Action.BET:
            return "bet"
        if self == Action.RAISE:
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
