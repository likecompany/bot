from __future__ import annotations

import time

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from likeinterface import Interface
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import AdjustGame, GetGame

from enums import Round
from keyboards import players_game_inline_keyboard_builder
from logger import logger
from schemas import Session, Settings
from states import GameState


def start_text(settings: Settings) -> str:
    return (
        f"Texas Holdem Poker\n"
        f"Stacksize: {settings.small_blind * 2 * settings.big_blind_multiplication}\n\n"
        f"Small Blind: {settings.small_blind}\n"
        f"Big Blind: {settings.small_blind * 2}"
    )


async def start_game(
    bot: Bot,
    inline_message_id: int,
    state: FSMContext,
    interface: Interface,
    session: Session,
    settings: Settings,
) -> None:
    if session.started:
        return logger.info(
            "(inline_message_id=%s) Start not available, because game is started, skipping..."
            % inline_message_id
        )

    players = len(session.game.players)
    if settings.min_players <= players <= settings.max_players:
        session.ready_to_start = True

    if not session.ready_to_start:
        await bot.edit_message_text(
            inline_message_id=inline_message_id,
            text=start_text(settings=settings),
            reply_markup=players_game_inline_keyboard_builder().as_markup(),
        )
        session.start_at = None

        return logger.info(
            "(inline_message_id=%s) Start not available, because game is not ready to start, skipping..."
            % inline_message_id
        )

    if players < settings.min_players:
        if session.ready_to_start:
            await bot.edit_message_text(
                inline_message_id=inline_message_id,
                text=start_text(settings=settings) + "Game doesn't start, not enough players...",
            )

        session.ready_to_start = False
        session.start_at = None

    if not session.start_at:
        session.start_at = time.time() + settings.start_time

    current_time = time.time()
    if session.start_at <= current_time:
        try:
            await interface.request(
                method=AdjustGame(
                    access=session.access, is_new_game=session.game.round == Round.SHOWDOWN.value
                )
            )
        except LikeInterfaceError:
            session.started = False

            await state.set_state(GameState.game_in_chat)
        else:
            session.started = True
            session.last_known_round = None

            await state.set_state(GameState.game_in_progress)
        finally:
            session.last_known_current_player = None
            session.ready_to_start = False
            session.start_at = None

            session.game = await interface.request(method=GetGame(access=session.access))

        return None

    await bot.edit_message_text(
        inline_message_id=inline_message_id,
        text=start_text(settings=settings)
        + f"The game will start in {session.start_at - current_time} seconds",
    )

    return None
