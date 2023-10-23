from __future__ import annotations

from typing import Any, Dict, Optional, Sequence, Union
from urllib import parse

from aiogram import Router
from aiogram.filters import CommandObject, CommandStart, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.payload import decode_payload
from likeinterface import types

from filters import TexasHoldemPokerFilter
from keyboards.exit import exit_inline_keyboard_builder
from schemas import LastKnownMessage, TexasHoldemPoker
from states import GameState
from utils.find_if import find_if

router = Router()


class CommandArgsFilter(Filter):
    def __init__(self, args: Optional[Sequence] = None) -> None:
        self.args = args

    async def __call__(
        self, message: Message, command: Optional[CommandObject]
    ) -> Union[bool, Dict[str, Any]]:
        if not command or not command.args:
            return False

        args = parse.parse_qsl(decode_payload(command.args))

        if self.args and not all(element in self.args for element in args):
            return False

        return {"args": args}


@router.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    await message.answer(text="Welcome! I'm the bot that can help you play poker in your groups.")


@router.message(
    CommandStart(),
    CommandArgsFilter(args=["game", "join"]),
    TexasHoldemPokerFilter(),
)
async def start_join_toi_game_handler(
    message: Message,
    state: FSMContext,
    user: types.User,
    session: TexasHoldemPoker,
) -> None:
    if find_if(collection=session.players, condition=lambda element: element.id == user.id):
        await message.answer("You Already In The Game!")

    message = await message.answer(
        text="You've Join To Game...", reply_markup=exit_inline_keyboard_builder().as_markup()
    )
    last_known_message = LastKnownMessage(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=message.text,
        reply_markup=message.reply_markup,
        state=GameState.in_game,
    )

    await state.update_data(last_known_message=last_known_message.model_dump())
    await state.set_state(state=GameState.in_game)
