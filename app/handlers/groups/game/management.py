from __future__ import annotations

import os

from aiogram import Bot, Router
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from likeinterface import Interface, types
from likeinterface.methods import AddGame, DeleteGame, GetGame

from callback_data import CardsCallbackData
from core.game import core
from enums import Round
from filters import IsOwner, SessionFilter, SettingsFilter, UserInGame
from keyboards import cards_inline_keyboard_builder
from schemas import Session, Settings
from states import GameState
from utils.cards import Cards

router = Router()


@router.message(
    Command(commands="create"),
    or_f(default_state, GameState.no_state),
    IsOwner(),
    SettingsFilter(),
)
async def create_game_handler(
    message: Message,
    bot: Bot,
    state: FSMContext,
    interface: Interface,
    scheduler: AsyncIOScheduler,
    settings: Settings,
) -> None:
    access = os.urandom(256).hex()

    await interface.request(
        method=AddGame(
            access=access,
            sb_bet=settings.small_blind_bet,
            bb_bet=settings.small_blind_bet * 2,
            bb_mult=settings.big_blind_multiplication,
            min_raise=settings.small_blind_bet * 2,
        )
    )

    await state.set_state(GameState.game_in_chat)
    await message.answer(
        text=f"Available new game\n\n"
        f"Stacksize: {settings.small_blind_bet * 2 * settings.big_blind_multiplication}\n\n"
        f"Small Blind: {settings.small_blind_bet}\n"
        f"Big Blind: {settings.small_blind_bet * 2}",
    )

    game = await interface.request(method=GetGame(access=access))

    session = Session(
        access=access,
        game=game,
        cards=Cards(),
    )
    await state.update_data(**session.model_dump())

    scheduler.add_job(
        core,
        kwargs={
            "scheduler": scheduler,
            "job_id": access,
            "bot": bot,
            "chat_id": message.chat.id,
            "state": state,
            "interface": interface,
            "settings": settings,
        },
        trigger="interval",
        id=access,
        max_instances=1,
        seconds=1,
    )


@router.message(
    Command(commands="delete"),
    or_f(GameState.game_in_chat, GameState.game_finished),
    IsOwner(),
    SessionFilter(),
)
async def delete_game_handler(
    message: Message,
    state: FSMContext,
    interface: Interface,
    user: types.User,
    session: Session,
) -> None:
    await interface.request(method=DeleteGame(access=session.access))

    await state.set_state(GameState.no_state)
    await message.answer(text="Game was deleted")


@router.message(
    Command(commands="cards"),
    or_f(GameState.game_in_progress, GameState.game_finished),
)
async def cards_handler(message: Message) -> None:
    await message.answer(
        text="To view cards press button",
        reply_markup=cards_inline_keyboard_builder().as_markup(),
    )


@router.callback_query(
    CardsCallbackData.filter(),
    or_f(GameState.game_in_progress, GameState.game_finished),
    SessionFilter(),
    UserInGame(),
)
async def cards_callback_query_handler(
    callback_query: CallbackQuery,
    session: Session,
    position: int,
) -> None:
    SLICE = (
        2 + session.game.round
        if Round.FLOP.value <= session.game.round <= Round.RIVER.value
        else 5
    )

    await callback_query.answer(
        text="Board: "
        + (
            " ".join(card.as_string_pretty() for card in session.board[:SLICE])
            if session.board and session.game.round != Round.PREFLOP.value
            else "There is no board cards yet"
        )
        + "\n\nHand: "
        + (
            " ".join(card.as_string_pretty() for card in session.players[position].hand)
            if session.players[position].hand
            else "There is no cards yet"
        ),
        show_alert=True,
    )
