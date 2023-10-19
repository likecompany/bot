from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery

from callback_data import CardsCallbackData
from filters import PlayerInGame, SessionFilter
from schemas import Player, Session

router = Router()


@router.callback_query(
    CardsCallbackData.filter(),
    SessionFilter(),
    PlayerInGame(),
)
async def cards_handler(
    callback_query: CallbackQuery,
    session: Session,
    player: Player,
) -> None:
    await callback_query.answer(
        text="Board: "
        + (
            " ".join(card.as_string_pretty() for card in session.board)
            if session.board
            else "There is no board cards yet"
        )
        + "\n\nHand: "
        + (
            " ".join(card.as_string_pretty() for card in player.hand)
            if player.hand
            else "There is no cards yet"
        ),
        show_alert=True,
    )
