from __future__ import annotations

from aiogram import Router, html
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from likeinterface import Interface
from likeinterface.enums import Action as AAction
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import ExecuteAction, GetPossibleActions
from likeinterface.types import Action, Game

from exc import CommandUsageError, InvalidActionError
from filters import GameFilter, UserIsCurrent, UserIsLeft
from states import GameState

router = Router()


@router.message(
    Command(commands=["check", "fold", "call", "bet", "allin"]),
    GameState.game_in_progress,
    GameFilter(),
    UserIsCurrent(),
    ~UserIsLeft(),
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
        raise InvalidActionError()

    to_execute = (
        AAction.CHECK
        if command.command == "check"
        else AAction.FOLD
        if command.command == "fold"
        else AAction.CALL
        if command.command == "call"
        else AAction.BET
        if command.command == "bet"
        else AAction.ALLIN
    )

    for action in actions:
        if to_execute == action.action:
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
    ~UserIsLeft(),
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
                    action=AAction.RAISE,
                    position=game.current,
                ),
            ),
        )
    except LikeInterfaceError:
        raise InvalidActionError()

    await message.answer(text="Action executed")
