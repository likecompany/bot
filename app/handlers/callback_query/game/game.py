from aiogram import Router

from .create import router as create_router
from .exit import router as exit_router
from .join import router as join_router

router = Router()
router.include_routers(create_router, exit_router, join_router)
