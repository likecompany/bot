from __future__ import annotations

from aiogram import Bot

from keyboards import game_inline_keyboard_builder
from logger import logger
from schemas import Session

from .round import round_text


async def adjust_round(
    bot: Bot,
    inline_message_id: int,
    redis_callback_data_key: str,
    session: Session,
) -> None:
    if not session.started:
        return logger.info(
            "(inline_message_id=%s) Game is in invalid state, skipping..." % inline_message_id
        )

    await bot.edit_message_text(
        text=round_text(session=session),
        inline_message_id=inline_message_id,
        reply_markup=game_inline_keyboard_builder(
            redis_callback_data_key=redis_callback_data_key
        ).as_markup(),
    )

    return None
