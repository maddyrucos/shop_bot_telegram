from aiogram.dispatcher.filters.state import State, StatesGroup

class Buy(StatesGroup):

    description = State()
    buying = State()
    default = State()
    deposit = State()

class Comment(StatesGroup):

    basic = State()
    comment = State()