from __future__ import annotations

from aiogram import Bot
from likeinterface import Interface

from enums import Round


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
