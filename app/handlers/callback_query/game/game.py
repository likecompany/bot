from aiogram import Router

from .actions import router as actions_router
from .create import router as create_router
from .exit import router as exit_router
from .join import router as join_router

router = Router()
router.include_routers(actions_router, create_router, exit_router, join_router)
