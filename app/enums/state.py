from __future__ import annotations

from enum import Enum

from likeinterface import enums


class State(Enum):
    INIT = enums.State.INIT.value
    OUT = enums.State.OUT.value
    ALIVE = enums.State.ALIVE.value
    ALLIN = enums.State.ALLIN.value

    def to_string_pretty(self) -> str:
        if self == State.INIT:
            return "🆓"
        if self.value == State.OUT:
            return "⛔️"
        if self.value == State.ALIVE:
            return "✅"

        return "🔪"
