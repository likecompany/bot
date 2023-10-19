from __future__ import annotations

from likeinterface import Interface
from likeinterface.methods import GetUser

from schemas import Player, Session
from utils.find_if import find_if


async def update_players(
    interface: Interface,
    session: Session,
) -> None:
    for position, player in enumerate(session.game.players):
        if not find_if(
            collection=session.players, condition=lambda element: element.id == player.id
        ):
            session.players.append(
                Player(
                    position=position,
                    user=await interface.request(method=GetUser(user_id=player.id)),
                    **player.model_dump(),
                )
            )

    session.players = [
        Player(
            position=position,
            user=await interface.request(method=GetUser(user_id=player.id)),
            hand=session.players[position].hand,
            **player.model_dump(),
        )
        for position, player in enumerate(session.game.players)
    ]
