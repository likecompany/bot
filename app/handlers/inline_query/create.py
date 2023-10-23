from __future__ import annotations

from typing import List

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.types import (
    InlineQuery,
    InlineQueryResult,
    InlineQueryResultArticle,
    InputTextMessageContent,
    User,
)

from keyboards import create_game_inline_keyboard_builder

router = Router()


def get_results(user: User) -> List[InlineQueryResult]:
    return [
        InlineQueryResultArticle(
            id=str(user.id),
            title="Texas Holdem Poker",
            input_message_content=InputTextMessageContent(
                message_text="Create Texas Holdem Poker Game TexasHoldemPoker"
            ),
            reply_markup=create_game_inline_keyboard_builder().as_markup(),
        )
    ]


@router.inline_query(
    ~F.query,
    F.chat_type.in_([ChatType.GROUP, ChatType.SUPERGROUP]),
)
async def create_game_handler(inline_query: InlineQuery) -> None:
    await inline_query.answer(results=get_results(user=inline_query.from_user))
