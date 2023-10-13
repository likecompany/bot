from __future__ import annotations

import datetime
from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject, User
from likeinterface import Interface
from likeinterface.methods import GetBalance, GetMe

from utils.authorization import create_telegram_authorization


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        interface: Optional[Interface] = data.get("interface")
        event_user: Optional[User] = data.get("event_user")

        if not interface or not event_user:
            return await handler(event, data)

        authorization = await interface.request(
            method=create_telegram_authorization(
                id=event_user.id,
                first_name=event_user.first_name,
                last_name=event_user.last_name,
                username=event_user.username,
                auth_date=datetime.datetime.utcnow(),
            ),
        )

        user = await interface.request(method=GetMe(access_token=authorization.access_token))
        balance = await interface.request(
            method=GetBalance(access_token=authorization.access_token)
        )

        return await handler(event, {"user": user, "balance": balance, **data})


def create_update_middleware(dispatcher: Dispatcher) -> None:
    dispatcher.update.middleware(UserMiddleware())


def create_middleware(dispatcher: Dispatcher) -> None:
    create_update_middleware(dispatcher=dispatcher)
