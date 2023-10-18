from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery

from callback_data import ActionsCallbackData
from enums import Action
from filters import PlayerInGame, PlayerIsCurrent, SessionFilter
from schemas import Player, Session

router = Router()


@router.callback_query(
    ActionsCallbackData.filter(),
    SessionFilter(),
    PlayerInGame(),
    PlayerIsCurrent(),
)
async def exit_from_game(
    callback_query: CallbackQuery,
    session: Session,
    player: Player,
) -> None:
    await callback_query.answer(
        text="\n".join(
            Action(action.action).to_string().capitalize()
            if action.action in [Action.FOLD.value, Action.CHECK.value]
            else f"{Action(action.action).to_string().capitalize()} - from {session.game.min_raise} to {player.behind}"
            if action.action == Action.RAISE.value
            else f"{Action(action.action).to_string().capitalize()} - {action.amount}"
            for action in session.actions
        ),
        show_alert=True,
    )
