from aiogram import F, Router
from aiogram.enums import ChatType

from .game import router as game_router

router = Router()
router.message.filter(F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
router.include_routers(game_router)
