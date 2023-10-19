from aiogram import Router

from .actions import router as actions_router
from .create import router as create_router

router = Router()
router.include_routers(actions_router, create_router)
