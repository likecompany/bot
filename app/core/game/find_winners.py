from __future__ import annotations

from typing import Optional

from likeinterface import Interface, types
from likeinterface.methods import GetEvaluationResult, SetNextGame

from enums import Round, State
from logger import logger
from schemas import Session
from utils.count_if import count_if
from utils.find_if import find_if


def get_cards(session: Session) -> Optional[types.Cards]:
    if (
        count_if(
            collection=session.players, condition=lambda element: element.state == State.OUT.value
        )
        == len(session.players) - 1
    ):
        return None

    return types.Cards(
        board=map(str, session.board),
        hands=[str().join(map(str, player.hand)) for player in session.players],
    )


async def get_winners_text(
    interface: Interface,
    session: Session,
    cards: Optional[types.Cards],
) -> Optional[str]:
    if not cards:
        return None

    winners = await interface.request(method=GetEvaluationResult(cards=cards))

    return "\n".join(
        f"{session.players[hand.id].mention_html()} - {hand.hand.title()}" for hand in winners
    )


async def find_winners(
    inline_message_id: int,
    interface: Interface,
    session: Session,
) -> None:
    if not session.started or session.game.round != Round.SHOWDOWN.value:
        return logger.info(
            "(inline_message_id=%s) Find winners not available, because game in invalid state, skipping..."
            % inline_message_id
        )

    cards = get_cards(session=session)

    winners = await get_winners_text(
        interface=interface,
        session=session,
        cards=cards,
    )

    session.winners = (
        winners
        if winners
        else f"There is only one winner - {find_if(collection=session.players, condition=lambda x: x.state in [State.ALIVE.value, State.ALLIN]).mention_html()}"
    )

    await interface.request(method=SetNextGame(access=session.access, cards=cards))

    session.started = False

    return None
