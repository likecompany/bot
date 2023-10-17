from __future__ import annotations

from aiogram import F, Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

router = Router()


@router.inline_query(~F.query)
async def create_game_handler(inline_query: InlineQuery) -> None:
    input_message_content: Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]

    await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                id=inline_query.from_user.id,
                title="Texas Holdem",
                input_message_content=[
                    InputTextMessageContent(message_text="Create Texas Holdem Game Session")
                ],
                reply_markup=...,
            )
        ],
    )
