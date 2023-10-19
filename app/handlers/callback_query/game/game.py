from aiogram import Router

from .actions import router as actions_router
from .cards import router as cards_router
from .create import router as create_router
from .exit import router as exit_router
from .join import router as join_router
from .players import router as players_router
from .winners import router as winners_router

router = Router()
router.include_routers(
    actions_router,
    cards_router,
    create_router,
    exit_router,
    join_router,
    players_router,
    winners_router,
)
