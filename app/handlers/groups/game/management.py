from __future__ import annotations

import os
import textwrap
from contextlib import suppress

from aiogram import Bot, Router
from aiogram.filters import Command, or_f
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from likeinterface import Interface
from likeinterface.enums import Action, Round, State
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import (
    AddGame,
    AdjustGame,
    DeleteGame,
    ExecuteAction,
    GetBalance,
    GetEvaluationResult,
    GetGame,
    GetPossibleActions,
    SetNextGame,
)
from likeinterface.methods.set_balance import SetBalance
from likeinterface.types import Cards, Game
from pydantic import ValidationError

from exc import AdjustError
from filters import (
    GameFilter,
    GameInformation,
    Owner,
    PlayerInformation,
    Settings,
    SettingsFilter,
    UserInGame,
)
from states import GameState
from utils.cards_generator import CardsGenerator
from utils.user import get_user_link

router = Router()


class GameCardsCallbackData(CallbackData, prefix="gamecards"):
    view_hand: bool


@router.message(
    Command(commands="create"),
    or_f(default_state, GameState.no_state),
    Owner(),
    SettingsFilter(),
)
async def create_game_handler(
    message: Message,
    state: FSMContext,
    interface: Interface,
    settings: Settings,
) -> None:
    sb_bet, bb_bet = settings.small_blind_bet, settings.small_blind_bet * 2

    game_access = os.urandom(256).hex()

    await interface.request(
        method=AddGame(
            access=game_access,
            sb_bet=sb_bet,
            bb_bet=bb_bet,
            bb_mult=settings.big_blind_multiplication,
            min_raise=bb_bet,
        )
    )

    await state.set_state(GameState.game_in_chat)
    await state.set_data({"game_access": game_access})

    await message.answer(
        text=f"Available new game\n\n"
        f"Stacksize: {bb_bet * settings.big_blind_multiplication}\n\n"
        f"Small Blind: {sb_bet}\n"
        f"Big Blind: {bb_bet}",
    )


@router.message(
    Command(commands="adjust"),
    or_f(GameState.game_in_chat, GameState.game_finished),
    GameFilter(),
    Owner(),
)
async def adjust_game_handler(
    message: Message,
    bot: Bot,
    state: FSMContext,
    interface: Interface,
    scheduler: AsyncIOScheduler,
    game: Game,
    game_access: str,
) -> None:
    try:
        await interface.request(
            method=AdjustGame(
                access=game_access,
                is_new_game=game.round == Round.SHOWDOWN,
            )
        )
    except LikeInterfaceError:
        raise AdjustError()

    game_information = GameInformation(
        cards_generator=CardsGenerator(),
        players=[
            PlayerInformation(position=position, user_id=player.id)
            for position, player in enumerate(game.players)
        ],
    )

    await state.set_state(GameState.game_in_progress)
    await state.update_data(**game_information.model_dump())

    await message.answer(text="Game was started")

    scheduler.add_job(
        core,
        kwargs={
            "scheduler": scheduler,
            "job_id": game_access,
            "bot": bot,
            "chat_id": message.chat.id,
            "state": state,
            "interface": interface,
            "game_access": game_access,
        },
        trigger="interval",
        id=game_access,
        max_instances=1,
        seconds=1,
    )


@router.message(
    Command(commands="delete"),
    or_f(GameState.game_in_chat, GameState.game_finished),
    GameFilter(),
    Owner(),
)
async def delete_game_handler(
    message: Message,
    state: FSMContext,
    interface: Interface,
    game: Game,
    game_access: str,
) -> None:
    await interface.request(method=DeleteGame(access=game_access))

    if await state.get_state() == GameState.game_in_chat.state:
        for player in game.players:
            balance = await interface.request(method=GetBalance(user_id=player.id))
            await interface.request(
                method=SetBalance(user_id=balance.user.id, balance=balance.balance + player.stack)
            )

    await state.set_state(GameState.no_state)
    await message.answer(text="Game was deleted")


@router.message(
    Command(commands="round"),
    or_f(GameState.game_in_progress, GameState.game_finished),
    GameFilter(),
)
async def round_handler(
    message: Message,
    interface: Interface,
    game: Game,
    game_information: GameInformation,
) -> None:
    def player_state_to_string(state: int) -> str:
        state = State(state)

        if state == State.INIT:
            return "action not posted"
        if state == State.OUT:
            return "out from game"
        if state == State.ALIVE:
            return "alive"
        if state == State.ALLIN:
            return "allin"

        return "unknown"

    await message.answer(
        text=f"Round - {game.round}\n\n"
        f"Current: {await get_user_link(interface=interface, user_id=game.players[game.current].id)}\n\n"
        f"Players:\n"
        + "\n\n".join(
            [
                f"{await get_user_link(interface=interface, user_id=player.user_id)}, "
                f"is left - {game.players[player.position].is_left}, "
                f"chips - {game.players[player.position].behind}, "
                f"round bet - {game.players[player.position].round_bet}, "
                f"game bet - {game.players[player.position].front}, "
                f"state - {player_state_to_string(game.players[player.position].state)}"
                for player in game_information.players
            ]
        )
    )


def gamecards_inline_keyboard_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Board", callback_data=GameCardsCallbackData(view_hand=False).pack()
        ),
        InlineKeyboardButton(
            text="My Cards", callback_data=GameCardsCallbackData(view_hand=True).pack()
        ),
    )

    return builder


@router.message(
    Command(commands="cards"),
    or_f(GameState.game_in_progress, GameState.game_finished),
)
async def cards_handler(message: Message) -> None:
    await message.answer(
        text="To view cards press any button",
        reply_markup=gamecards_inline_keyboard_builder().as_markup(),
    )


@router.callback_query(
    GameCardsCallbackData.filter(),
    or_f(GameState.game_in_progress, GameState.game_finished),
    GameFilter(),
    UserInGame(),
)
async def cards_callback_query_handler(
    callback_query: CallbackQuery,
    callback_data: GameCardsCallbackData,
    game: Game,
    game_information: GameInformation,
    player: PlayerInformation,
) -> None:
    if callback_data.view_hand:
        await callback_query.answer(
            text=player.cards if player.cards else "There is no cards yet",
            show_alert=True,
        )
    else:
        SLICE = (2 + game.round) if Round.FLOP.value <= game.round <= Round.RIVER.value else 5
        await callback_query.answer(
            text=game_information.board[0 : (SLICE * 2)]
            if game_information.board or game.round == Round.PREFLOP
            else "There is no board cards yet",
            show_alert=True,
        )


async def core(
    scheduler: AsyncIOScheduler,
    job_id: int,
    bot: Bot,
    chat_id: int,
    state: FSMContext,
    interface: Interface,
    game_access: str,
    hand_size: int = 2,
    board_size: int = 5,
) -> None:
    data = await state.get_data()

    try:
        game = await interface.request(method=GetGame(access=game_access))
    except LikeInterfaceError:
        return scheduler.remove_job(job_id=job_id)

    game_information = GameInformation.model_validate(data)

    if game.round != Round.PREFLOP.value:
        if not game_information.board:
            game_information.board = str().join(
                game_information.cards_generator.deal(n=board_size)
            )

        for player in game_information.players:
            if not player.cards and game.players[player.position].state != State.OUT.value:
                player.cards = str().join(game_information.cards_generator.deal(n=hand_size))

    if game.round == Round.SHOWDOWN.value:
        try:
            cards = Cards(
                board=textwrap.fill(game_information.board, 2).split("\n"),
                hands=[player.cards for player in game_information.players],
            )
        except ValidationError:
            cards = text = None
        else:
            winners = await interface.request(method=GetEvaluationResult(cards=cards))
            text = "\n".join(
                [
                    f"{hand.hand.title()} - {await get_user_link(interface=interface, user_id=game.players[hand.id].id)}"
                    for hand in winners
                ]
            )

        await interface.request(method=SetNextGame(access=game_access, cards=cards))

        game = await interface.request(method=GetGame(access=game_access))

        for player in game_information.players:
            balance = await interface.request(method=GetBalance(user_id=player.user_id))
            await interface.request(
                method=SetBalance(
                    user_id=player.user_id,
                    balance=balance.balance + game.players[player.position].stack,
                )
            )

        if text:
            await bot.send_message(chat_id=chat_id, text=f"Winners:\n{text}")
        else:
            await bot.send_message(
                chat_id=chat_id, text="All players are outs, there is only 1 winner"
            )
            for player in game.players:
                if player.state in [State.ALIVE, State.ALLIN]:
                    await bot.send_message(
                        chat_id=chat_id,
                        text=f"Player - {await get_user_link(interface)} is winner",
                    )

        await bot.send_message(chat_id=chat_id, text="Game was ended")
        await state.set_state(GameState.game_finished)

        return scheduler.remove_job(job_id=job_id)

    if game.players[game.current].is_left:
        possible_actions = await interface.request(method=GetPossibleActions(access=game_access))

        to_execute = None
        for action in possible_actions:
            if action.action == Action.CHECK.value:
                to_execute = action
            if action.action == Action.FOLD.value and not to_execute:
                to_execute = action

        with suppress(Exception):
            await interface.request(method=ExecuteAction(access=game_access, action=to_execute))

    await state.update_data(**game_information.model_dump())

    return None
