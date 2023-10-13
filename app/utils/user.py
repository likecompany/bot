from __future__ import annotations

from aiogram import html
from aiogram.utils.link import create_tg_link
from likeinterface import Interface
from likeinterface.methods import GetUser


async def get_user_link(interface: Interface, user_id: int) -> str:
    user = await interface.request(method=GetUser(user_id=user_id))

    return html.link(user.username, create_tg_link("user", id=user.telegram_id))
