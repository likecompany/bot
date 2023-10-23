from __future__ import annotations

from aiogram import Router

from .create import router as create_router


def setup() -> Router:
    router = Router()

    router.include_routers(create_router)

    return router
