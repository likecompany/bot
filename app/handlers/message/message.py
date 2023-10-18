from aiogram import Router

from .balance import router as balance_router
from .evaluate import router as evaluate_router
from .settings import router as settings_router
from .start import router as start_router

router = Router()
router.include_routers(balance_router, evaluate_router, settings_router, start_router)
