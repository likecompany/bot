from __future__ import annotations

from likeinterface import Interface
from likeinterface.enums import Position, Round, State
from likeinterface.types import Game

from filters import GameInformation
from utils.state import player_state_to_string
from utils.user import get_user_link


def round_to_string(value: Round) -> str:
    if value == Round.PREFLOP:
        return "preflop"
    if value == Round.FLOP:
        return "flop"
    if value == Round.TURN:
        return "turn"
    if value == Round.RIVER:
        return "river"

    return "showdown"


async def get_round_text(
    interface: Interface,
    game: Game,
    game_information: GameInformation,
) -> str:
    return (
        f"{round_to_string(Round(game.round)).capitalize()}\n\n"
        + f"Small Blind: {await get_user_link(interface=interface, user_id=game.players[Position.SB.value].id)}\n"
        + f"Big Blind: {await get_user_link(interface=interface, user_id=game.players[Position.BB.value].id)}\n"
        + f"Current: {await get_user_link(interface=interface, user_id=game.players[game.current].id)}\n\n"
        + "Players:\n"
        + "\n\n".join(
            [
                f"{await get_user_link(interface=interface, user_id=player.user_id)}, "
                f"is left - {game.players[player.position].is_left}, "
                f"chips - {game.players[player.position].behind}, "
                f"round bet - {game.players[player.position].round_bet}, "
                f"game bet - {game.players[player.position].front}, "
                f"state - {player_state_to_string(State(game.players[player.position].state))}"
                for player in game_information.players
            ]
        )
    )
