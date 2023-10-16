from __future__ import annotations

from enum import Enum

from likeinterface import enums


class State(Enum):
    INIT = enums.State.INIT.value
    OUT = enums.State.OUT.value
    ALIVE = enums.State.ALIVE.value
    ALLIN = enums.State.ALLIN.value

    def to_string(self) -> str:
        if self.value == enums.State.INIT.value:
            return "action not posted"
        if self.value == enums.State.OUT.value:
            return "out from game"
        if self.value == enums.State.ALIVE.value:
            return "alive"

        return "allin"
