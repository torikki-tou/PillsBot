from aiogram.dispatcher.filters.state import State, StatesGroup


class Dialog(StatesGroup):
    new_pill_title = State()
    new_pill_time = State()
    new_pill_save = State()
