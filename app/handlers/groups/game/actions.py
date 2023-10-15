from __future__ import annotations

from aiogram import Router, html
from aiogram.filters import Command, CommandObject, invert_f
from aiogram.types import Message
from likeinterface import Interface, enums, types
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import ExecuteAction

from enums import Action
from exc import CommandUsageError, InvalidActionError
from filters import SessionFilter, UserIsCurrent, UserIsLeft
from schemas import Session
from states import GameState

router = Router()


@router.message(
    Command(commands=["check", "fold", "call", "bet", "allin"]),
    GameState.game_in_progress,
    SessionFilter(),
    UserIsCurrent(),
    invert_f(UserIsLeft()),
)
async def actions_without_args_handler(
    message: Message,
    command: CommandObject,
    interface: Interface,
    session: Session,
) -> None:
    to_execute = None
    for action in session.actions:
        if Action.from_string(command.command).value == action.action:
            to_execute = action

    if not to_execute:
        raise InvalidActionError()

    await interface.request(method=ExecuteAction(access=session.access, action=to_execute))
    await message.answer(text="You've posted action")


@router.message(
    Command(commands="raise"),
    GameState.game_in_progress,
    SessionFilter(),
    UserIsCurrent(),
    invert_f(UserIsLeft()),
)
async def raise_actions_handler(
    message: Message,
    command: CommandObject,
    interface: Interface,
    session: Session,
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
                access=session.access,
                action=types.Action(
                    amount=amount,
                    action=enums.Action.RAISE.value,
                    position=session.game.current,
                ),
            ),
        )
    except LikeInterfaceError:
        raise InvalidActionError()

    await message.answer(text="You've posted action")
