from __future__ import annotations

from aiogram import Router
from aiogram.filters import invert_f
from aiogram.types import CallbackQuery
from likeinterface import Interface, types
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import JoinToGame

from callback_data import JoinCallbackData
from exc import JoinError
from filters import PlayerInGame, SessionFilter
from schemas import Session

router = Router()


@router.callback_query(
    JoinCallbackData.filter(),
    SessionFilter(),
    invert_f(PlayerInGame()),
)
async def join_to_game(
    callback_query: CallbackQuery,
    interface: Interface,
    user: types.User,
    session: Session,
) -> None:
    try:
        await interface.request(
            method=JoinToGame(access=session.access, id=user.id, stacksize=20000)
        )
    except LikeInterfaceError:
        raise JoinError()

    await callback_query.answer(text="You've join to game")
