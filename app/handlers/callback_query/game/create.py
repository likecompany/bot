from __future__ import annotations

import uuid

from aiogram import Bot, Router
from aiogram.types import CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from likeinterface import Interface
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import AddGame
from redis.asyncio.client import Redis

from callback_data import CreateGameCallbackData
from core.game import game
from logger import logger
from schemas import Settings

router = Router()


@router.callback_query(CreateGameCallbackData.filter())
async def create_game_handler(
    callback_query: CallbackQuery,
    bot: Bot,
    scheduler: AsyncIOScheduler,
    redis: Redis,
    interface: Interface,
    settings: Settings,
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

    await callback_query.answer(text="Successfully created")

    return scheduler.add_job(
        game,
        kwargs={
            "scheduler": scheduler,
            "job_id": access,
            "access": access,
            "bot": bot,
            "inline_message_id": callback_query.inline_message_id,
            "redis": redis,
            "redis_callback_data_key": redis_callback_data_key,
            "interface": interface,
            "settings": settings,
        },
        trigger="interval",
        id=access,
        max_instances=1,
        seconds=1,
    )
