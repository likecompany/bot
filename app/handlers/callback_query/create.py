from __future__ import annotations

import uuid

from aiogram import Router
from aiogram.types import CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from likeinterface import Interface
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import AddGame
from redis.asyncio.client import Redis

from callback_data import CreateGameCallbackData
from enums import Game
from filters import As
from keyboards import join_inline_keyboard_builder
from logger import logger
from schemas import Settings

router = Router()


async def create_texas_holdem_poker(
    callback_query: CallbackQuery,
    redis: Redis,
    interface: Interface,
    settings: Settings,
    scheduler: AsyncIOScheduler,
) -> None:
    access = uuid.uuid4().hex
    redis_callback_data_key = uuid.uuid4().hex

    await redis.set(name=redis_callback_data_key, value=access)

    try:
        await interface.request(
            method=AddGame(
                access=access,
                sb_bet=settings.small_blind,
                bb_bet=settings.small_blind * 2,
                bb_mult=settings.big_blind_multiplication,
                min_raise=settings.small_blind * 2,
            ),
        )
    except LikeInterfaceError as e:
        logger.exception(e)

        return await callback_query.answer(text="Failed to create game")

    await callback_query.bot.edit_message_text(
        inline_message_id=callback_query.inline_message_id,
        text=f"Texas Holdem Poker\n\n"
        f"Stack: {settings.small_blind * 2 * settings.big_blind_multiplication}\n\n"
        f"SB/BB: {settings.small_blind}/{settings.small_blind * 2}",
        reply_markup=join_inline_keyboard_builder(
            bot=callback_query.bot,
            redis_callback_data_key=redis_callback_data_key,
            game=Game.TEXAS_HOLDEM_POKER.value,
        ).as_markup(),
    )
    return None


@router.callback_query(
    CreateGameCallbackData.filter(),
    As(Settings, "settings"),
)
async def create_game_handler(
    callback_query: CallbackQuery,
    callback_data: CreateGameCallbackData,
    redis: Redis,
    interface: Interface,
    settings: Settings,
    scheduler: AsyncIOScheduler,
) -> None:
    if callback_data.game == Game.TEXAS_HOLDEM_POKER.value:
        return await create_texas_holdem_poker(
            callback_query=callback_query,
            redis=redis,
            interface=interface,
            settings=settings,
            scheduler=scheduler,
        )

    return await callback_query.answer(text="Sorry, Game Not Supported Yet!")
