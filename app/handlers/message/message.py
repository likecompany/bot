from __future__ import annotations

from aiogram import Router

from .balance import router as balance_router
from .evaluate import router as evaluate_router
from .start import router as start_router


def setup() -> Router:
    router = Router()

    router.include_routers(balance_router, evaluate_router, start_router)

    return router
