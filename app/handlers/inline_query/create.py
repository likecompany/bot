from __future__ import annotations

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from keyboards import create_game_inline_keyboard_builder

router = Router()


@router.inline_query(
    ~F.query,
    F.chat_type.in_([ChatType.GROUP, ChatType.SUPERGROUP]),
)
async def create_game_handler(inline_query: InlineQuery) -> None:
    await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                id=str(inline_query.from_user.id),
                title="Texas Holdem Poker",
                input_message_content=InputTextMessageContent(
                    message_text="Create Texas Holdem Poker Game Session"
                ),
                reply_markup=create_game_inline_keyboard_builder().as_markup(),
            )
        ],
    )
