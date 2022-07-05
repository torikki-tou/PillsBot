from aiogram.dispatcher.filters.state import State, StatesGroup


class Dialog(StatesGroup):
    new_pill_name = State()
    new_pill_time = State()
