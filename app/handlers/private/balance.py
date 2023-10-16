from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from likeinterface.types import Balance

router = Router()


@router.message(Command(commands="balance"))
async def balance_command_handler(message: Message, balance: Balance) -> None:
    await message.reply(
        text=f"Your balance is: {balance.balance}, if you wanna to up it just play in poker!"
    )
