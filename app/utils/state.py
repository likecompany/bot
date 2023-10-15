from __future__ import annotations

from likeinterface.enums import State


def player_state_to_string(state: State) -> str:
    if state == State.INIT:
        return "action not posted"
    if state == State.OUT:
        return "out from game"
    if state == State.ALIVE:
        return "alive"
    if state == State.ALLIN:
        return "allin"

    return "unknown"
