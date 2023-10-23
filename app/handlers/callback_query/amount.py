from __future__ import annotations

from contextlib import suppress
from typing import List

from aiogram import Bot, Router
from aiogram.exceptions import TelegramAPIError, TelegramNotFound
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from callback_data.edit_amount import EditAmountCallbackData
from enums import State
from keyboards.pin import pin_inline_keyboard_builder
from schemas import LastKnownMessage, Pin
from states import PinState
from utils.message import back_to_preview_message

router = Router()


@router.callback_query(
    EditAmountCallbackData.filter(),
    default_state,
)
async def edit_amount_handler(
    callback_query: CallbackQuery,
    callback_data: EditAmountCallbackData,
    state: FSMContext,
    scheduler: AsyncIOScheduler,
) -> None:
    await state.update_data(pin=Pin(key=callback_data.key, attribute=callback_data.attribute))
    await state.set_state(state=PinState.enter_pin)

    scheduler.add_job(
        update_value_task,
        kwargs={
            "scheduler": scheduler,
            "job_id": callback_data.job_id(user=callback_query.from_user),
            "bot": callback_query.bot,
            "callback_data": callback_data,
            "state": state,
            "close_on": [default_state, PinState.confirm],
            "pin_key": "pin",
        },
        trigger="interval",
        id=callback_data.job_id(user=callback_query.from_user),
        seconds=0.1,
    )


async def update_value_task(
    scheduler: AsyncIOScheduler,
    job_id: str,
    bot: Bot,
    callback_data: EditAmountCallbackData,
    state: FSMContext,
    close_on: List[State],
    pin_key: str,
) -> None:
    data = await state.get_data()

    if await state.get_state() in close_on or not data:
        await back_to_preview_message(
            bot=bot,
            state=state,
            last_known_message=LastKnownMessage.model_validate(data.get("last_known_message")),
        )

        return scheduler.remove_job(job_id=job_id)

    pin = Pin.model_validate(data.get(pin_key))

    last_known_pin = data.get("last_known_pin")
    if pin != Pin.model_validate(last_known_pin):
        await state.update_data(last_known_pin=pin.model_dump())

        try:
            await bot.edit_message_text(
                text=f"Amount: {pin.value if pin.value else 'Nothing'}",
                chat_id=callback_data.chat_id,
                message_id=callback_data.message_id,
                inline_message_id=callback_data.inline_message_id,
                reply_markup=pin_inline_keyboard_builder().as_markup(),
            )
        except TelegramNotFound:
            with suppress(TelegramAPIError):
                await back_to_preview_message(
                    bot=bot,
                    state=state,
                    last_known_message=LastKnownMessage.model_validate(
                        data.get("last_known_message")
                    ),
                )

            return scheduler.remove_job(job_id=job_id)
    return None
