from __future__ import annotations

from enums import Round
from schemas import Session


def round_text(session: Session) -> str:
    return f"Round - {Round(session.game.round).to_string().capitalize()}"
