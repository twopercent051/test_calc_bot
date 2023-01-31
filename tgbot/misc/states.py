from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMUser(StatesGroup):
    home = State()
    numbers = State()

