from __future__ import annotations

import asyncio

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from aioschedule import run_pending
from likeinterface import Interface, Network
from redis.asyncio.client import Redis

from core.middleware import create_middleware
from core.settings import fsm_settings, interface_settings
from handlers import router as handlers_router


def create_dispatcher() -> Dispatcher:
    interface = Interface(network=Network(base=interface_settings.INTERFACE_BASE))

    dispatcher = Dispatcher(
        storage=RedisStorage(
            redis=Redis(host=fsm_settings.FSM_HOSTNAME, port=fsm_settings.FSM_PORT),
        ),
        fsm_strategy=FSMStrategy.CHAT,
        interface=interface,
    )
    dispatcher.include_router(handlers_router)

    def create_on_event() -> None:
        @dispatcher.startup()
        async def scheduler() -> None:
            async def _scheduler() -> None:
                while True:
                    await run_pending()
                    await asyncio.sleep(0.1)

            asyncio.create_task(_scheduler())

        @dispatcher.shutdown()
        async def shutdown_interface(interface: Interface) -> None:
            await interface.session.close()

    create_middleware(dispatcher=dispatcher)
    create_on_event()

    return dispatcher
