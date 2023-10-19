from __future__ import annotations

from typing import List

from aiogram import Router
from aiogram.types import CallbackQuery

from callback_data import PlayersCallbackData
from enums import Position, State
from filters import SessionFilter
from schemas import Session

router = Router()


def players_text(session: Session) -> List[str]:
    text = "{position} {username} {state} - 💲{chips}, bet 💲{round_bet}"

    return [
        text.format(
            position=Position(player.position).to_string_pretty(),
            username=player.user.username,
            state=State(player.state).to_string_pretty(),
            chips=player.behind,
            round_bet=player.round_bet,
        )
        for player in session.players
    ]


@router.callback_query(
    PlayersCallbackData.filter(),
    SessionFilter(),
)
async def game_players_handler(
    callback_query: CallbackQuery,
    session: Session,
) -> None:
    await callback_query.answer(
        text="\n".join(players_text(session=session)),
        show_alert=True,
    )
