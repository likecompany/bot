from aiogram import Router

from .groups import router as groups_router
from .private import router as private_router

router = Router()
router.include_routers(groups_router, private_router)
