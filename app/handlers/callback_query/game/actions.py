from __future__ import annotations

from contextlib import suppress

from aiogram import Router
from aiogram.exceptions import TelegramAPIError
from aiogram.types import CallbackQuery
from likeinterface import Interface, types
from likeinterface.methods import ExecuteAction

from callback_data import ActionsCallbackData, ExecuteActionCallbackData
from enums import Action
from filters import PlayerInGame, PlayerIsCurrent, SessionFilter
from schemas import Session

router = Router()


@router.callback_query(
    ActionsCallbackData.filter(),
    SessionFilter(),
    PlayerInGame(),
    PlayerIsCurrent(),
)
async def actions_handler(callback_query: CallbackQuery, session: Session) -> None:
    await callback_query.answer(
        text="\n".join(
            Action(action.action).to_string().capitalize()
            if action.action in [Action.FOLD.value, Action.CHECK.value]
            else f"{Action(action.action).to_string().capitalize()} - from {session.game.min_raise} to {action.amount}"
            if action.action == Action.RAISE.value
            else f"{Action(action.action).to_string().capitalize()} - {action.amount}"
            for action in session.actions
        ),
        show_alert=True,
    )


@router.callback_query(
    ExecuteActionCallbackData.filter(),
    SessionFilter(),
    PlayerInGame(),
    PlayerIsCurrent(),
)
async def execute_action_handler(
    callback_query: CallbackQuery,
    callback_data: ExecuteActionCallbackData,
    interface: Interface,
    session: Session,
) -> None:
    await interface.request(
        method=ExecuteAction(
            access=session.access,
            action=types.Action(
                action=callback_data.action,
                amount=callback_data.amount,
                position=callback_data.position,
            ),
        )
    )

    with suppress(TelegramAPIError):
        await callback_query.message.delete()

    await callback_query.answer(text="Successfully")

    session.action_end_at = None
