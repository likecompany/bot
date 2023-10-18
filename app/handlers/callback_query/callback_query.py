from aiogram import Router

from .game import router as game_router

router = Router()
router.include_routers(game_router)
