from __future__ import annotations

from aiogram import Router

from .amount import router as amount_router
from .back import router as back_router
from .pin import router as pin_router
from .settings import router as settings_router


def setup() -> Router:
    router = Router()

    router.include_routers(amount_router, back_router, pin_router, settings_router)

    return router
