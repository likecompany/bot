from aiogram import Router

from .create import router as create_router

router = Router()
router.include_routers(create_router)
