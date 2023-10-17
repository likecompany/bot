from __future__ import annotations

from enums import Round
from logger import logger
from schemas import Session


async def deal_cards(
    chat_id: int,
    session: Session,
    reset: bool = False,
    hand_size: int = 2,
    board_size: int = 5,
) -> None:
    if not session.started and session.game.round != Round.SHOWDOWN.value:
        return logger.info("(chat_id=%s) Game is in invalid state, skipping..." % chat_id)

    if session.game.round == Round.PREFLOP.value:
        for player in session.players:
            if not player.hand:
                player.hand = session.cards.deal(n=hand_size)

    if session.game.round != Round.PREFLOP.value:
        if not session.board:
            session.board = session.cards.deal(n=board_size)

    if reset:
        logger.info(
            "(chat_id=%s) Cards: BOARD %s, HANDS %s"
            % (chat_id, session.board, [player.hand for player in session.players])
        )

        session.cards.reset()
        session.board.clear()

        return None

    return None
