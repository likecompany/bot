from __future__ import annotations

import time

from likeinterface import Interface
from likeinterface.exceptions import LikeInterfaceError
from likeinterface.methods import ExecuteAction, GetPossibleActions

from enums import Action, Round
from logger import logger
from schemas import Session, Settings


async def possible_actions(
    inline_message_id: int,
    interface: Interface,
    session: Session,
) -> None:
    if not session.started or session.game.round == Round.SHOWDOWN.value:
        return logger.info(
            "(inline_message_id=%s) Find winners not available, because game in invalid state, skipping..."
            % inline_message_id
        )

    try:
        session.actions = await interface.request(method=GetPossibleActions(access=session.access))
    except LikeInterfaceError:
        logger.warning(
            "(inline_message_id=%s) Skipping get possible actions..." % inline_message_id
        )
        raise


async def auto_execute_action(
    inline_message_id: int,
    interface: Interface,
    session: Session,
    settings: Settings,
) -> None:
    if not session.started or session.game.round == Round.SHOWDOWN.value:
        return logger.info(
            "(inline_message_id=%s) Nothing to do in the auto action" % inline_message_id
        )

    if not session.action_end_at:
        session.action_end_at = time.time() + settings.action_time

    if session.action_end_at <= time.time():
        logger.info(
            "(inline_message_id=%s) Player action time is ended, "
            "engine will found **check** or **fold** (**check** in the priority)"
            % inline_message_id
        )

        execute = None
        for action in session.actions:
            if action.action == Action.FOLD.value:
                execute = action
            if action.action == Action.CHECK.value:
                execute = action
                logger.info(
                    "(inline_message_id=%s) Action **check** was found, rejecting **fold**"
                    % inline_message_id
                )

        if not execute:
            return logger.critical(
                "(inline_message_id=%s) Action for game in chat not found!" % inline_message_id
            )

        await interface.request(method=ExecuteAction(access=session.access, action=execute))
        logger.info("(inline_message_id=%s) Player auto action completed" % inline_message_id)

        session.action_end_at = None

    return None
