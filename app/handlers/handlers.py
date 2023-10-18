from aiogram import Router

from .callback_query import router as callback_query_router
from .inline_query import router as inline_query_router
from .message import router as message_router

router = Router()
router.include_routers(callback_query_router, inline_query_router, message_router)
