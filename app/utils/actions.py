from __future__ import annotations

from typing import List

from likeinterface import Interface
from likeinterface.enums import Action as AAction
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import GetPossibleActions
from likeinterface.types import Action, Game

from exc import NoPossibleActionsError


def action_to_string(value: AAction) -> str:
    if value == AAction.CHECK:
        return "check"
    if value == AAction.FOLD:
        return "fold"
    if value == AAction.CALL:
        return "call"
    if value == AAction.BET:
        return "bet"
    if value == AAction.RAISE:
        return "raise"

    return "allin"


def string_to_action(value: str) -> AAction:
    if value == "check":
        return AAction.CHECK
    if value == "fold":
        return AAction.FOLD
    if value == "call":
        return AAction.CALL
    if value == "bet":
        return AAction.BET
    if value == "raise":
        return AAction.RAISE

    return AAction.ALLIN


async def get_possible_actions(interface: Interface, game_access: str) -> List[Action]:
    try:
        return await interface.request(method=GetPossibleActions(access=game_access))
    except LikeInterfaceError:
        raise NoPossibleActionsError()


async def get_possible_actions_text(
    interface: Interface,
    game: Game,
    game_access: str,
) -> str:
    actions = await get_possible_actions(interface=interface, game_access=game_access)

    return (
        "No actions available"
        if not actions
        else "Actions:\n"
        + "\n".join(
            action_to_string(AAction(action.action)).capitalize()
            if action.action == AAction.FOLD
            else f"{action_to_string(AAction(action.action)).capitalize()} - from {game.min_raise} to {game.players[game.current].behind}"
            if action.action == AAction.RAISE.value
            else f"{action_to_string(AAction(action.action)).capitalize()} - {action.amount}"
            for action in actions
        )
    )
