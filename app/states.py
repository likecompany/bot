from aiogram.fsm.state import State, StatesGroup


class GameState(StatesGroup):
    no_state = State()
    update_settings = State()
    game_in_chat = State()
    game_in_progress = State()
    game_finished = State()
