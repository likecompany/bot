from __future__ import annotations

import textwrap
from typing import List, Tuple, Union

from aiogram import Router, html
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from likeinterface import Interface, methods
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.types import Cards

from exc import CommandUsageError

router = Router()


def validate_command_args(args: str) -> Union[Tuple[List[str], List[str]], bool]:
    if not args:
        return False

    try:
        board, *hands = args.split()
    except ValueError:
        return False

    board = textwrap.fill(board, 2).split("\n")
    return board, hands


@router.message(Command(commands="evaluate"))
async def evaluate_command_handler(
    message: Message,
    command: CommandObject,
    interface: Interface,
) -> None:
    args = validate_command_args(command.args)
    if not args:
        raise CommandUsageError(
            html.quote(
                f"Usage: {command.prefix}{command.command} {html.bold('[board]')} {html.bold('[hand]')} {html.bold('[hand]')}\n"
                f"Example {html.code(f'{command.prefix}{command.command} AcAdAhAsKc 2c2d 2h2s')}"
            ),
        )

    board, hands = args

    try:
        text = "\n".join(
            f"{hand.hand.title()} - {html.bold(hands[hand.id])}"
            for hand in await interface.request(
                method=methods.GetEvaluationResult(cards=Cards(board=board, hands=hands))
            )
        )
    except LikeInterfaceError:
        await message.answer(text="Invalid arguments")
    else:
        await message.answer(text=html.quote(text))
