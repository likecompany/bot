from __future__ import annotations

import os

from aiogram import Router
from aiogram.types import CallbackQuery
from likeinterface import Interface
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import AddGame

from callback_data import CreateGameCallbackData
from logger import logger
from schemas import Settings

router = Router()


@router.callback_query(CreateGameCallbackData.filter())
async def create_game_handler(
    callback_query: CallbackQuery,
    interface: Interface,
    settings: Settings,
) -> None:
    access = os.urandom(256).hex()

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
