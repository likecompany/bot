from __future__ import annotations

from enums import Round
from logger import logger
from schemas import Session


async def deal_cards(
    inline_message_id: int,
    session: Session,
    reset: bool = False,
    hand_size: int = 2,
    board_size: int = 5,
) -> None:
    if not session.started:
        return logger.info(
            "(inline_message_id=%s) Game not started, skipping..." % inline_message_id
        )

    if session.game.round == Round.PREFLOP.value:
        for player in session.players:
            if not player.hand:
                player.hand = session.cards.deal(n=hand_size)

    if session.game.round != Round.PREFLOP.value:
        if not session.board:
            session.board = session.cards.deal(
                n=session.game.round + 2
                if session.game.round != Round.SHOWDOWN.value
                else board_size
            )
        else:
            session.board += session.cards.deal(
                n=session.game.round - 1 if session.game.round != Round.SHOWDOWN else 0
            )

    if reset:
        logger.info(
            "(inline_message_id=%s) Cards: BOARD %s, HANDS %s"
            % (inline_message_id, session.board, [player.hand for player in session.players])
        )

        session.cards.reset()
        session.board.clear()

        return None

    return None
