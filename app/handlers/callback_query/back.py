from __future__ import annotations

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from callback_data.back import BackCallbackData
from filters import As
from schemas import LastKnownMessage
from utils.message import back_to_preview_message

router = Router()


@router.callback_query(
    BackCallbackData.filter(),
    As(LastKnownMessage, "last_known_message"),
)
async def back_callback_handler(
    callback_query: CallbackQuery,
    state: FSMContext,
    last_known_message: LastKnownMessage,
) -> None:
    await back_to_preview_message(
        bot=callback_query.bot,
        state=state,
        last_known_message=last_known_message,
    )
