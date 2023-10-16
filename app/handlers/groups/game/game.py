from aiogram import Router

from .actions import router as actions_router
from .management import router as management_router
from .player import router as player_router
from .settings import router as settings_router

router = Router()
router.include_routers(actions_router, management_router, player_router, settings_router)
