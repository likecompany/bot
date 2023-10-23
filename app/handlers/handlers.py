from __future__ import annotations

from aiogram import Router

from .callback_query import setup_callback_query
from .inline_query import setup_inline_query
from .message import setup_message


def setup() -> Router:
    router = Router()

    callback_query_router = setup_callback_query()
    inline_query_router = setup_inline_query()
    message_router = setup_message()

    router.include_routers(callback_query_router, inline_query_router, message_router)

    return router
