from aiogram.fsm.state import State, StatesGroup


class CreateSpending(StatesGroup):
    name = State()
    money = State()
    date = State()
    id = State()
    update = State()


class GetSpendings(StatesGroup):
    up_date = State()
    to_date = State()


class DeleteSpendings(StatesGroup):
    get_id = State()
