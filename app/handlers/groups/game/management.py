from __future__ import annotations

import os
from contextlib import suppress

from aiogram import Bot, Router
from aiogram.filters import Command, or_f
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aioschedule import CancelJob, every
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
        f"Stacksize: {bb_bet * settings.small_blind_bet}\n\n"
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
    await state.update_data(game_information=game_information)

    await message.answer(text="Game was started")

    every().second.do(
        core,
        bot=bot,
        chat_id=message.chat.id,
        state=state,
        interface=interface,
        game_access=game_access,
    )


@router.message(
    Command(commands="delete"),
    or_f(GameState.game_in_chat, GameState.game_finished),
    Owner(),
)
async def delete_game_handler(
    message: Message,
    state: FSMContext,
    interface: Interface,
) -> None:
    data = await state.get_data()

    await interface.request(method=DeleteGame(access=data["game_access"]))

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
    def player_state_to_string(state: State) -> str:
        if state == State.INIT:
            return "action not posted"
        if state == State.OUT:
            return "out from game"
        if state == State.ALIVE:
            return "alive"
        if state == "allin":
            return "allin"

        return "unknown"

    await message.answer(
        text=f"Round {game.round}:\n".join(
            f"{await get_user_link(interface=interface, user_id=player.user_id)}, "
            f"is left - {game.players[player.position].is_left}, "
            f"chips - {game.players[player.position].behind}, "
            f"round bet - {game.players[player.position].round_bet}, "
            f"game bet - {game.players[player.position].front}, "
            f"state - {player_state_to_string(game.players[player.position].state)}"
            f""
            for player in game_information.players
        ),
    )


def gamecards_inline_keyboard_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Board", callback_data=GameCardsCallbackData(view_hand=False)),
        InlineKeyboardButton(text="My Cards", callback_data=GameCardsCallbackData(view_hand=True)),
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
        SLICE = 1 + game.round if 1 <= game.round <= 3 else 4
        await callback_query.answer(
            text=game_information.board[0::SLICE]
            if game_information.board or game.round == Round.PREFLOP
            else "There is no board cards yet",
            show_alert=True,
        )


async def core(
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
        return CancelJob

    cards_generator = data["cards_generator"]
    game_information = GameInformation.model_validate(data["game_information"])

    if game.round != Round.PREFLOP:
        for player in game_information.players:
            if not player.cards and not game.players[player.position].is_left:
                player.cards = str().join(cards_generator.deal(n=hand_size))

    if not game_information.board:
        game_information.board = str().join(cards_generator.deal(n=board_size))

    if game.round == Round.SHOWDOWN:
        cards = Cards(
            board=game_information.board,
            hands=[player.cards for player in game_information.players],
        )
        winners = await interface.request(method=GetEvaluationResult(cards=cards))
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

        await bot.send_message(chat_id=chat_id, text="Game was ended")
        text = "\n".join(
            f"{hand.hand.title()} - {await get_user_link(interface=interface, user_id=game.players[hand.id].id)}"
            for hand in winners
        )
        await bot.send_message(chat_id=chat_id, text=f"Winners:\n{text}")
        await state.set_state(GameState.game_finished)

        return CancelJob

    if game[game.current.value].is_left:
        possible_actions = await interface.request(method=GetPossibleActions(access=game_access))

        to_execute = None
        for action in possible_actions:
            if action.action == Action.CHECK:
                to_execute = action
            if action.action == Action.FOLD and not to_execute:
                to_execute = action

        with suppress(Exception):
            await interface.request(method=ExecuteAction(access=game_access, action=to_execute))
            return None
    return None
