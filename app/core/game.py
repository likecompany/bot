from __future__ import annotations

import time

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from likeinterface import Interface, types
from likeinterface.enums import Position
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import (
    AdjustGame,
    ExecuteAction,
    GetBalance,
    GetEvaluationResult,
    GetGame,
    GetPossibleActions,
    GetUser,
    SetNextGame,
)
from likeinterface.methods.set_balance import SetBalance
from pydantic import ValidationError

from enums import Action, Round, State
from keyboards import cards_inline_keyboard_builder
from logger import logger
from schemas import Player, Session, Settings
from states import GameState


async def find_winners(
    bot: Bot,
    chat_id: int,
    state: FSMContext,
    interface: Interface,
    session: Session,
    board_size: int = 5,
) -> None:
    if not session.started or session.game.round != Round.SHOWDOWN.value:
        return logger.info(
            "(chat_id=%s) Find winners not available, because game in invalid state, skipping..."
            % chat_id
        )

    cards = types.Cards(
        board=map(str, session.board),
        hands=[str().join(map(str, player.hand)) for player in session.players],
    )
    if len(session.board) != board_size:
        cards = None

    count = 1
    for player in session.game.players:
        if player.state == State.OUT:
            count += 1

    if count == len(session.game.players):
        cards = None

    try:
        winners = await interface.request(method=GetEvaluationResult(cards=cards))
    except ValidationError:
        cards = text = None
    else:
        text = "\n".join(
            f"{session.players[hand.id].mention_html()} - {hand.hand.title()}" for hand in winners
        )

    await interface.request(method=SetNextGame(access=session.access, cards=cards))
    game = await interface.request(method=GetGame(access=session.access))

    await bot.send_message(chat_id=chat_id, text="Players chips after game")
    for position, player in enumerate(session.players):
        balance = await interface.request(method=GetBalance(user_id=player.user.id))
        await interface.request(
            method=SetBalance(
                user_id=player.user.id,
                balance=balance.balance + game.players[position].stack,
            )
        )

        await bot.send_message(
            chat_id=chat_id,
            text=f"{player.mention_html()} - before: {player.player.stack}, after {game.players[position].stack}, difference {game.players[position].stack - player.player.stack}",
        )

    if cards and text:
        await bot.send_message(chat_id=chat_id, text=f"Winners:\n{text}")
    else:
        await bot.send_message(
            chat_id=chat_id, text="All players are outs, there is only 1 winner"
        )
        for position, player in enumerate(game.players):
            if player.state == State.ALIVE.value:
                await bot.send_message(
                    chat_id=chat_id,
                    text=f"{session.players[position].mention_html()} - is winner",
                )

    session.started = False
    session.game = game

    await bot.send_message(chat_id=chat_id, text="Game was ended")
    await state.set_state(GameState.game_finished)

    return None


async def round_message(
    bot: Bot,
    chat_id: int,
    session: Session,
) -> None:
    if not session.started or session.game.round == Round.SHOWDOWN.value:
        return logger.info("(chat_id=%s) Game is in invalid state, skipping..." % chat_id)

    if session.last_known_round != session.game.round:
        session.last_known_round = session.game.round
        session.last_known_current_player = None

        await bot.send_message(
            chat_id=chat_id,
            text=f"Round: {Round(session.game.round).to_string().capitalize()}",
            reply_markup=cards_inline_keyboard_builder().as_markup(),
        )

        if session.game.round == Round.PREFLOP:
            await bot.send_message(
                chat_id=chat_id,
                text="Blinds\n\n"
                f"{session.players[Position.SB.value].mention_html()} - Small Blind\n"
                f"{session.players[Position.BB.value].mention_html()} - Big Blind\n",
            )
            return None
        return None

    return None


async def auto_execute_action(
    bot: Bot,
    chat_id: int,
    interface: Interface,
    session: Session,
) -> None:
    if not session.started or session.game.round == Round.SHOWDOWN.value:
        return logger.info("(chat_id=%s) Nothing to do in the auto action" % chat_id)

    player = session.players[session.game.current]
    if (game_player := session.game.players[session.game.current]) and not game_player.is_left:
        return logger.info(
            "(chat_id=%s) Player [%s] is not left, skipping..." % (chat_id, player.user.id)
        )

    logger.info(
        "(chat_id=%s) Player [%s] is left, engine will found **check** or **fold** (**check** in the priority)"
        % (chat_id, player.user.id)
    )

    execute = None
    for action in session.actions:
        if action.action == Action.FOLD.value:
            execute = action
        if action.action == Action.CHECK.value:
            execute = action
            logger.info("(chat_id=%s) Action **check** was found, rejecting **fold**" % chat_id)

    if not execute:
        return logger.critical("(chat_id=%s) Action for game in chat not found!" % chat_id)

    await interface.request(method=ExecuteAction(access=session.access, action=execute))
    await bot.send_message(chat_id=chat_id, text=f"{player.mention_html()} auto action completed")

    logger.info("(chat_id=%s) Player [%s] auto action completed" % (chat_id, game_player.id))
    return None


async def wait_for_player_action(
    bot: Bot,
    chat_id: int,
) -> None:
    ...


async def core(
    scheduler: AsyncIOScheduler,
    job_id: int,
    bot: Bot,
    chat_id: int,
    state: FSMContext,
    interface: Interface,
    settings: Settings,
) -> None:
    session = Session.model_validate(await state.get_data())

    try:
        session.game = await interface.request(method=GetGame(access=session.access))
    except LikeInterfaceError:
        logger.info("(chat_id=%s) Game was delete" % chat_id)
        return scheduler.remove_job(job_id=job_id)

    try:
        session.actions = await interface.request(method=GetPossibleActions(access=session.access))
    except LikeInterfaceError:
        logger.info("(chat_id=%s) skipping get possible actions...")

    await find_winners(bot=bot, chat_id=chat_id, interface=interface, state=state, session=session)
    await start_game(
        bot=bot,
        chat_id=chat_id,
        state=state,
        interface=interface,
        session=session,
        settings=settings,
    )
    await round_message(bot=bot, chat_id=chat_id, session=session)
    await deal_cards(
        chat_id=chat_id, session=session, reset=session.game.round == Round.SHOWDOWN.value
    )
    await current_player_message(bot=bot, chat_id=chat_id, session=session)
    await auto_execute_action(bot=bot, chat_id=chat_id, interface=interface, session=session)

    await state.update_data(**session.model_dump())

    return None
