from __future__ import annotations

from likeinterface import Interface
from likeinterface.methods import GetUser

from logger import logger
from schemas import Player, Session


async def update_players(
    inline_message_id: int,
    interface: Interface,
    session: Session,
) -> None:
    if session.started:
        return logger.info(
            "(inline_message_id=%s) Game started, skipping..." % inline_message_id
        )

    session.players = [
        Player(
            position=position,
            user=await interface.request(method=GetUser(user_id=player.id)),
            **player.model_dump(),
        )
        for position, player in enumerate(session.game.players)
    ]

    return None
