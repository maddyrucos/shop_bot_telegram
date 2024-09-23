from aiogram.dispatcher.filters.state import State, StatesGroup

class Buy(StatesGroup):

    description = State()
    buying = State()
    default = State()
    deposit = State()

class Comment(StatesGroup):

    basic = State()
    comment = State()

class Admin(StatesGroup):

    default = State()
    sending_message = State()
    name = State()
    cost = State()
    code = State()
    category = State()
    description = State()
    photo = State()
    end = State()
    apply = State()
