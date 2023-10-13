from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from likeinterface import Interface
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import JoinToGame, LeftFromGame
from likeinterface.methods.set_balance import SetBalance
from likeinterface.types import Balance, Game

from exc import JoinError, NotEnoughBalanceError
from filters import GameFilter, PlayerInformation, UserInGame
from states import GameState

router = Router()


@router.message(
    Command(commands="join"),
    GameState.game_in_chat,
    GameFilter(),
    ~UserInGame(),
)
async def join_to_game_handler(
    message: Message,
    interface: Interface,
    balance: Balance,
    game: Game,
    game_access: str,
) -> None:
    stacksize = game.bb_bet * game.bb_mult
    if balance.balance < stacksize:
        raise NotEnoughBalanceError(balance.balance, stacksize)

    try:
        await interface.request(
            method=JoinToGame(access=game_access, id=balance.user.id, stacksize=stacksize)
        )
    except LikeInterfaceError:
        raise JoinError()

    await message.reply(text="You've join to game")
    await interface.request(
        method=SetBalance(user_id=balance.user.id, balance=balance.balance - stacksize)
    )


@router.message(
    Command(commands="exit"),
    or_f(GameState.game_in_chat, GameState.game_finished, GameState.game_in_progress),
    GameFilter(),
    UserInGame(),
)
async def left_from_not_started_game_handler(
    message: Message,
    state: FSMContext,
    interface: Interface,
    balance: Balance,
    game: Game,
    game_access: str,
    player: PlayerInformation,
) -> None:
    try:
        await interface.request(method=LeftFromGame(access=game_access, position=player.position))
    finally:
        chat_state = await state.get_state()
        if chat_state == GameState.game_in_progress:
            await message.reply(text="You've exit of the game, wait until game ended")
        else:
            if chat_state != GameState.game_finished.state:
                await interface.request(
                    method=SetBalance(
                        user_id=balance.user.id,
                        balance=balance.balance + game.players[player.position].stack,
                    )
                )
            await message.reply(text="You've exit of the game")
