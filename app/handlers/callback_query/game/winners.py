from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery

from callback_data import WinnersCallbackData
from filters import SessionFilter
from schemas import Session

router = Router()


@router.callback_query(
    WinnersCallbackData.filter(),
    SessionFilter(),
)
async def winners_handler(callback_query: CallbackQuery, session: Session) -> None:
    await callback_query.answer(text=session.winners, show_alert=True)
