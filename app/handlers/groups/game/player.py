from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, invert_f, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from likeinterface import Interface, types
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import JoinToGame, LeftFromGame
from likeinterface.methods.set_balance import SetBalance

from exc import JoinError, NotEnoughBalanceError
from filters import SessionFilter, UserInGame
from schemas import Session
from states import GameState

router = Router()


@router.message(
    Command(commands="join"),
    or_f(GameState.game_in_chat, GameState.game_finished),
    SessionFilter(),
    invert_f(UserInGame()),
)
async def join_to_game_handler(
    message: Message,
    interface: Interface,
    user: types.User,
    balance: types.Balance,
    session: Session,
) -> None:
    stacksize = session.game.bb_bet * session.game.bb_mult
    if balance.balance < stacksize:
        raise NotEnoughBalanceError(balance.balance, stacksize)

    try:
        await interface.request(
            method=JoinToGame(access=session.access, id=balance.user.id, stacksize=stacksize)
        )
    except LikeInterfaceError:
        raise JoinError()

    await interface.request(
        method=SetBalance(user_id=user.id, balance=balance.balance - stacksize)
    )
    await message.reply(text="You've join to game")


@router.message(
    Command(commands="exit"),
    or_f(GameState.game_in_chat, GameState.game_finished, GameState.game_in_progress),
    SessionFilter(),
    UserInGame(),
)
async def exit_from_game(
    message: Message,
    state: FSMContext,
    interface: Interface,
    user: types.User,
    balance: types.Balance,
    session: Session,
    position: int,
) -> None:
    try:
        await interface.request(method=LeftFromGame(access=session.access, position=position))
    finally:
        chat_state = await state.get_state()
        if chat_state == GameState.game_in_progress:
            await message.reply(text="You've exit of the game, wait until game ended")
        else:
            if chat_state != GameState.game_finished.state:
                await interface.request(
                    method=SetBalance(
                        user_id=user.id,
                        balance=balance.balance + session.players[position].stack,
                    )
                )
            await message.reply(text="You've exit of the game")
