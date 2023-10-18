from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from likeinterface import Interface
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import LeftFromGame

from callback_data import ExitCallbackData
from exc import ExitError
from filters import PlayerInGame, SessionFilter
from schemas import Player, Session

router = Router()


@router.callback_query(
    ExitCallbackData.filter(),
    SessionFilter(),
    PlayerInGame(),
)
async def exit_from_game(
    callback_query: CallbackQuery,
    interface: Interface,
    session: Session,
    player: Player,
) -> None:
    try:
        await interface.request(
            method=LeftFromGame(access=session.access, position=player.position)
        )
    except LikeInterfaceError:
        raise ExitError()

    await callback_query.answer(text="You've exit of the game")
