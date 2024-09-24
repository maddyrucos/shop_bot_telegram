from aiogram.fsm.state import StatesGroup, State

class User(StatesGroup):
    default = State()
    count = State()
    code = State()
    topup = State()