from __future__ import annotations

from aiogram import Router, html
from aiogram.filters import Command, CommandObject, invert_f
from aiogram.types import Message
from likeinterface import Interface
from likeinterface.enums import Action as AAction
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import ExecuteAction
from likeinterface.types import Action, Game

from exc import CommandUsageError, InvalidActionError
from filters import GameFilter, UserIsCurrent, UserIsLeft
from states import GameState
from utils.actions import (
    get_possible_actions,
    get_possible_actions_text,
    string_to_action,
)

router = Router()


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
    text = await get_possible_actions_text(interface=interface, game=game, game_access=game_access)
    await message.reply(text=text)


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
    actions = await get_possible_actions(interface=interface, game_access=game_access)

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
