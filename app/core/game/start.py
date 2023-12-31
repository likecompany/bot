from __future__ import annotations

import time
from contextlib import suppress

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from likeinterface import Interface
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import AdjustGame

from enums import Round
from keyboards import game_ended_inline_keyboard_builder
from keyboards.exit import exit_inline_keyboard_builder
from logger import logger
from schemas import Session, Settings


async def start_game(
    bot: Bot,
    inline_message_id: int,
    redis_callback_data_key: str,
    interface: Interface,
    session: Session,
    settings: Settings,
) -> None:
    if session.started:
        return logger.info(
            "(inline_message_id=%s) Start not available, because game is started, skipping..."
            % inline_message_id
        )

    players = len(session.players)
    if settings.min_players <= players <= settings.max_players:
        session.ready_to_start = True

    if not session.ready_to_start:
        session.start_at = None

        return logger.info(
            "(inline_message_id=%s) Start not available, because game is not ready to start, skipping..."
            % inline_message_id
        )

    if players < settings.min_players:
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
        else:
            session.winners = None
            session.started = True
        finally:
            session.ready_to_start = False
            session.start_at = None

        return None

    with suppress(TelegramBadRequest):
        await bot.edit_message_text(
            inline_message_id=inline_message_id,
            text=f"The game will start in {int(session.start_at - current_time)} seconds",
            reply_markup=exit_inline_keyboard_builder().as_markup()
            if not session.game.round == Round.SHOWDOWN.value
            else game_ended_inline_keyboard_builder().as_markup(),
        )

    return None
