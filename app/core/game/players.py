from __future__ import annotations

from likeinterface import Interface
from likeinterface.methods import GetUser

from schemas import Player, Session


async def update_players(
    interface: Interface,
    session: Session,
) -> None:
    session.players = [
        Player(
            position=position,
            user=await interface.request(method=GetUser(user_id=player.id)),
            **player.model_dump(),
        )
        for position, player in enumerate(session.game.players)
    ]
