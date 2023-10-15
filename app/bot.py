from __future__ import annotations

from contextlib import suppress

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError
from aiogram.types import (
    BotCommand,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    ChatAdministratorRights,
)

from core.settings import bot_settings


async def create_bot() -> Bot:
    bot = Bot(
        token=bot_settings.BOT_TOKEN,
        parse_mode=ParseMode.HTML,
    )
    with suppress(TelegramAPIError):
        await bot.set_my_default_administrator_rights(
            rights=ChatAdministratorRights(
                is_anonymous=False,
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=False,
                can_restrict_members=False,
                can_promote_members=False,
                can_change_info=True,
                can_invite_users=False,
                can_pin_messages=True,
            ),
        )

        await bot.set_my_commands(
            commands=[
                BotCommand(command="/start", description="🖐 Welcome message"),
                BotCommand(command="/evaluate", description="🧮 Evaluate Poker Hands"),
                BotCommand(command="/balance", description="💳 User Balance"),
            ],
            scope=BotCommandScopeAllPrivateChats(),
        )
        await bot.set_my_commands(
            commands=[
                BotCommand(command="/create", description="🃏 Create New Game (Owner Only)"),
                BotCommand(command="/delete", description="🃏 Delete Game (Owner Only)"),
                BotCommand(
                    command="/settings", description="⚙️ Game Create Settings (Owner Only)"
                ),
                BotCommand(command="/join", description="👨‍🦲 Join To Game"),
                BotCommand(command="/exit", description="👨‍🦲 Exit From Game"),
                BotCommand(command="/cards", description="🃏 Get Cards"),
                BotCommand(command="/fold", description="❗️ Poker Fold"),
                BotCommand(command="/check", description="❗️ Poker Check"),
                BotCommand(command="/call", description="❗️ Poker Call"),
                BotCommand(command="/bet", description="❗️ Poker Bet"),
                BotCommand(command="/raise", description="❗️ Poker Raise"),
                BotCommand(command="/allin", description="❗️ Poker Allin"),
            ],
            scope=BotCommandScopeAllGroupChats(),
        )

        await bot.set_my_description(
            description="Bot that help to play Texas Holdem Poker.\n\nFor support text to @copper_boy"
        )
        await bot.set_my_short_description(short_description="Play Texas Holdem Poker Now!")

        await bot.set_my_name(name="Texas Holdem Poker")

    return bot
