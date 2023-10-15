from __future__ import annotations

from likeinterface import enums


class State(enums.State):
    def to_string(self) -> str:
        if self == State.INIT:
            return "action not posted"
        if self == State.OUT:
            return "out from game"
        if self == State.ALIVE:
            return "alive"
        if self == State.ALLIN:
            return "allin"

        return "unknown"
