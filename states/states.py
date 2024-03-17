from aiogram.fsm.state import StatesGroup, State


class FSMInProgress(StatesGroup):
    progress = State()
