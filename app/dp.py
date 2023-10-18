from __future__ import annotations

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from likeinterface import Interface, Network
from redis.asyncio.client import Redis

from core.middleware import create_middleware
from core.settings import fsm_settings, interface_settings
from handlers import router as handlers_router


def create_dispatcher() -> Dispatcher:
    interface = Interface(network=Network(base=interface_settings.INTERFACE_BASE))
    scheduler = AsyncIOScheduler()
    redis = Redis(host=fsm_settings.FSM_HOSTNAME, port=fsm_settings.FSM_PORT)

    dispatcher = Dispatcher(
        storage=RedisStorage(redis=redis),
        fsm_strategy=FSMStrategy.USER_IN_CHAT,
        interface=interface,
        scheduler=scheduler,
        redis=redis,
    )
    dispatcher.include_router(handlers_router)

    def create_on_event() -> None:
        @dispatcher.startup()
        async def startup_scheduler(scheduler: AsyncIOScheduler) -> None:
            scheduler.start()

        @dispatcher.shutdown()
        async def shutdown_interface(interface: Interface) -> None:
            await interface.session.close()

    create_middleware(dispatcher=dispatcher)
    create_on_event()

    return dispatcher
