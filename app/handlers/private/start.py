from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    await message.answer(text="Welcome! I`m the bot that can help you play poker in your groups.")
