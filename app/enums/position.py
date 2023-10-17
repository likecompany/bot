from __future__ import annotations

from enum import Enum

from likeinterface import enums


class Position(Enum):
    SB = enums.Position.SB.value
    BB = enums.Position.BB.value
    UTG = enums.Position.UTG.value
    LWJ = enums.Position.LWJ.value
    HIJ = enums.Position.HIJ.value
    COF = enums.Position.COF.value
    BTN = enums.Position.BTN.value

    def to_string_pretty(self) -> str:
        if self == Position.SB:
            return "🇸🇧"
        if self == Position.BB:
            return "🇧🇧"
        if self == Position.UTG:
            return "🇺"
        if self == Position.LWJ:
            return "🇱"
        if self == Position.HIJ:
            return "🇭"
        if self == Position.COF:
            return "🇭"

        return ""
