from __future__ import annotations

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery

from callback_data import MySettingsCallbackData, SettingsCallbackData
from filters import As
from keyboards import settings_inline_keyboard_builder
from schemas import LastKnownMessage, Settings

router = Router()


@router.callback_query(
    MySettingsCallbackData.filter(),
    default_state,
    As(Settings, "settings", Settings()),
    As(LastKnownMessage, "last_known_message"),
)
async def my_settings_handler(
    callback_query: CallbackQuery,
    callback_data: MySettingsCallbackData,
    state: FSMContext,
    last_known_message: LastKnownMessage,
) -> None:
    last_known_message.bind_to = LastKnownMessage(
        chat_id=callback_data.chat_id,
        message_id=callback_data.message_id,
        inline_message_id=callback_data.inline_message_id,
        text="Here Is Your Create Game Settings",
        reply_markup=settings_inline_keyboard_builder(
            key="settings",
            chat_id=callback_data.chat_id,
            message_id=callback_data.message_id,
            inline_message_id=callback_data.inline_message_id,
        ).as_markup(),
    )

    await state.update_data(last_known_message=last_known_message.model_dump())

    await callback_query.bot.edit_message_text(
        chat_id=last_known_message.chat_id,
        message_id=last_known_message.message_id,
        inline_message_id=last_known_message.inline_message_id,
        text=last_known_message.bind_to.text,
        reply_markup=last_known_message.bind_to.reply_markup,
    )

    await callback_query.answer(text="Just Click Any Of Buttons")


@router.callback_query(
    SettingsCallbackData.filter(),
    As(Settings, "settings", Settings()),
)
async def view_settings_callback_data(
    callback_query: CallbackQuery,
    callback_data: SettingsCallbackData,
    settings: Settings,
) -> None:
    await callback_query.answer(
        text=f"{callback_data.text}: {getattr(settings, callback_data.attribute)}",
        show_alert=True,
    )
