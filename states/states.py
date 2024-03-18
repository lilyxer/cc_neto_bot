from aiogram.fsm.state import StatesGroup, State


class FSMInProgress(StatesGroup):
    progress = State()
    add_word = State()
    del_word = State()