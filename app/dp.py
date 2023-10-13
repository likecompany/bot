from __future__ import annotations

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from likeinterface import Interface, Network
from redis.asyncio.client import Redis

from core.settings import fsm_settings, interface_settings
from handlers import router as handlers_router


def create_dispatcher() -> Dispatcher:
    interface = Interface(network=Network(base=interface_settings.INTERFACE_BASE))

    dispatcher = Dispatcher(
        storage=RedisStorage(
            redis=Redis.from_url(fsm_settings.FSM_URL),
        ),
        fsm_strategy=FSMStrategy.CHAT,
        interface=interface,
    )
    dispatcher.include_router(handlers_router)

    @dispatcher.shutdown()
    async def shutdown_interface(interface: Interface) -> None:
        await interface.session.close()

    return dispatcher
