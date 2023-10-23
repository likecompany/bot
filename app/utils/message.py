from __future__ import annotations

from aiogram import Bot
from aiogram.fsm.context import FSMContext

from schemas import LastKnownMessage


async def back_to_preview_message(
    bot: Bot,
    state: FSMContext,
    last_known_message: LastKnownMessage,
) -> None:
    last_known_message = last_known_message.bind_to

    await bot.edit_message_text(
        chat_id=last_known_message.chat_id,
        message_id=last_known_message.message_id,
        inline_message_id=last_known_message.inline_message_id,
        text=last_known_message.text,
        reply_markup=last_known_message.reply_markup,
    )

    await state.set_state(state=last_known_message.state)
    await state.update_data(last_known_message=last_known_message.model_dump())
