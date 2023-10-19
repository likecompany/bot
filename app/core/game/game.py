from __future__ import annotations

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from likeinterface import Interface
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import GetGame
from redis.asyncio.client import Redis

from exc import CloseGameError
from logger import logger
from schemas import Session, Settings
from utils.cards import Cards

from .action import auto_execute_action, possible_actions
from .adjust_round import adjust_round
from .cards import deal_cards
from .find_winners import find_winners
from .players import update_players
from .start import start_game


async def set_game(
    scheduler: AsyncIOScheduler,
    job_id: int,
    inline_message_id: int,
    interface: Interface,
    session: Session,
) -> None:
    try:
        session.game = await interface.request(method=GetGame(access=session.access))
    except LikeInterfaceError:
        logger.info("(inline_message_id=%s) Game was delete" % inline_message_id)
        scheduler.remove_job(job_id=job_id)

        raise CloseGameError


async def core(
    scheduler: AsyncIOScheduler,
    job_id: int,
    bot: Bot,
    inline_message_id: int,
    redis_callback_data_key: str,
    interface: Interface,
    session: Session,
    settings: Settings,
) -> None:
    await set_game(
        scheduler=scheduler,
        job_id=job_id,
        inline_message_id=inline_message_id,
        interface=interface,
        session=session,
    )

    await update_players(interface=interface, session=session)

    await find_winners(inline_message_id=inline_message_id, interface=interface, session=session)

    await start_game(
        bot=bot,
        inline_message_id=inline_message_id,
        redis_callback_data_key=redis_callback_data_key,
        interface=interface,
        session=session,
        settings=settings,
    )

    await possible_actions(
        inline_message_id=inline_message_id, interface=interface, session=session
    )

    await adjust_round(
        bot=bot,
        inline_message_id=inline_message_id,
        redis_callback_data_key=redis_callback_data_key,
        session=session,
    )

    await deal_cards(
        inline_message_id=inline_message_id, session=session, reset=bool(session.winners)
    )

    await auto_execute_action(
        inline_message_id=inline_message_id,
        interface=interface,
        session=session,
        settings=settings,
    )


async def game(
    scheduler: AsyncIOScheduler,
    job_id: int,
    access: str,
    bot: Bot,
    inline_message_id: int,
    redis: Redis,
    redis_callback_data_key: str,
    interface: Interface,
    settings: Settings,
) -> None:
    session_json = await redis.get(name=access)

    session = (
        Session(access=access, cards=Cards())
        if not session_json
        else Session.model_validate_json(session_json)
    )

    try:
        await core(
            scheduler=scheduler,
            job_id=job_id,
            bot=bot,
            inline_message_id=inline_message_id,
            redis_callback_data_key=redis_callback_data_key,
            interface=interface,
            session=session,
            settings=settings,
        )
    except CloseGameError:
        return logger.info("(inline_message_id=%s) Closing job..." % inline_message_id)

    await redis.set(name=access, value=session.model_dump_json())

    return None
