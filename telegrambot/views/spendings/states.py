from aiogram.fsm.state import State, StatesGroup


class CreateSpending(StatesGroup):
    name = State()
    money = State()
    date = State()
