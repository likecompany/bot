from __future__ import annotations

from aiogram import Router, html
from aiogram.filters import Command, CommandObject, invert_f
from aiogram.types import Message
from likeinterface import Interface
from likeinterface.enums import Action as AAction
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import ExecuteAction, GetPossibleActions
from likeinterface.types import Action, Game

from exc import CommandUsageError, InvalidActionError, NoPossibleActionsError
from filters import GameFilter, UserIsCurrent, UserIsLeft
from states import GameState

router = Router()


def action_to_string(action: AAction) -> str:
    if action == AAction.CHECK.value:
        return "check"
    if action == AAction.FOLD.value:
        return "fold"
    if action == AAction.CALL.value:
        return "call"
    if action == AAction.BET.value:
        return "bet"
    if action == AAction.RAISE.value:
        return "raise"

    return "allin"


def string_to_action(string: str) -> AAction:
    if string == "check":
        return AAction.CHECK
    if string == "fold":
        return AAction.FOLD
    if string == "call":
        return AAction.CALL
    if string == "bet":
        return AAction.BET
    if string == "raise":
        return AAction.RAISE

    return AAction.ALLIN


@router.message(
    Command(commands="actions"),
    GameState.game_in_progress,
    GameFilter(),
    UserIsCurrent(),
    invert_f(UserIsLeft()),
)
async def actions_handler(
    message: Message,
    interface: Interface,
    game: Game,
    game_access: str,
) -> None:
    try:
        actions = await interface.request(method=GetPossibleActions(access=game_access))
    except LikeInterfaceError:
        raise NoPossibleActionsError()

    await message.reply(
        text="No actions"
        if not actions
        else "Actions:\n"
        + "\n".join(
            [
                f"{action_to_string(action.action).capitalize()} - {action.amount}"
                if action.action != AAction.RAISE.value
                else f"{action_to_string(action.action).capitalize()} - from {game.min_raise} to {game.players[game.current].behind}"
                for action in actions
            ]
        )
    )


@router.message(
    Command(commands=["check", "fold", "call", "bet", "allin"]),
    GameState.game_in_progress,
    GameFilter(),
    UserIsCurrent(),
    invert_f(UserIsLeft()),
)
async def actions_without_args_handler(
    message: Message,
    command: CommandObject,
    interface: Interface,
    game_access: str,
) -> None:
    try:
        actions = await interface.request(method=GetPossibleActions(access=game_access))
    except LikeInterfaceError:
        raise NoPossibleActionsError()

    to_execute = string_to_action(command.command)
    for action in actions:
        if to_execute.value == action.action:
            await interface.request(
                method=ExecuteAction(
                    access=game_access,
                    action=action,
                )
            )
            return await message.answer(text="Action executed")

    raise InvalidActionError()


@router.message(
    Command(commands="raise"),
    GameState.game_in_progress,
    GameFilter(),
    UserIsCurrent(),
    invert_f(UserIsLeft()),
)
async def raise_actions_handler(
    message: Message,
    command: CommandObject,
    interface: Interface,
    game: Game,
    game_access: str,
) -> None:
    try:
        amount = int(command.args)
    except ValueError:
        raise CommandUsageError(
            html.quote(f"Usage: {command.prefix}{command.command} {html.bold('[chips]')}")
        )

    try:
        await interface.request(
            method=ExecuteAction(
                access=game_access,
                action=Action(
                    amount=amount,
                    action=AAction.RAISE.value,
                    position=game.current,
                ),
            ),
        )
    except LikeInterfaceError:
        raise InvalidActionError()

    await message.answer(text="Action executed")
