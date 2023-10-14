from aiogram import F, Router
from aiogram.enums import ChatType

from .balance import router as balance_router
from .evaluate import router as evaluate_router
from .start import router as start_router

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)
router.include_routers(balance_router, evaluate_router, start_router)
