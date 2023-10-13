from aiogram import Router

from .evaluate import router as evaluate_router
from .groups import router as groups_router
from .private import router as private_router

router = Router()
router.include_routers(evaluate_router, groups_router, private_router)
