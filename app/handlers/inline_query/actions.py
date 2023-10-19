from __future__ import annotations

from aiogram import F, Router
from aiogram.enums import ChatType, ParseMode
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils import markdown
from likeinterface import types

from enums import Action
from filters import PlayerInGame, PlayerIsCurrent, SessionFilter
from keyboards import execute_action_inline_keyboard_builder
from schemas import Session

router = Router()


def get_action_amount(action: types.Action, session: Session) -> str:
    if action.action == Action.RAISE.value:
        return f"from {session.game.min_raise} to {action.amount}"

    return f"{action.amount}"


@router.inline_query(
    F.query.func(len) > 0,
    F.chat_type.in_([ChatType.GROUP, ChatType.SUPERGROUP]),
    SessionFilter(),
    PlayerInGame(),
    PlayerIsCurrent(),
)
async def actions_handler(
    inline_query: InlineQuery,
    session: Session,
    redis_callback_data_key: str,
) -> None:
    await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                id=Action(action.action).to_string(),
                title=f"{Action(action.action).to_string().capitalize()}: {get_action_amount(action=action, session=session)}",
                input_message_content=InputTextMessageContent(
                    message_text=f"Click button to execute {markdown.hbold(Action(action.action).to_string())}",
                    parse_mode=ParseMode.HTML,
                ),
                reply_markup=execute_action_inline_keyboard_builder(
                    action=action.action,
                    amount=action.amount,
                    position=action.position,
                    redis_callback_data_key=redis_callback_data_key,
                ).as_markup(),
            )
            for action in session.actions
        ],
    )
