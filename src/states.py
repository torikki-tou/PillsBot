from aiogram.dispatcher.filters.state import State, StatesGroup


class Dialog(StatesGroup):
    new_pill_title = State()
    new_pill_time = State()
    new_pill_save = State()
    update_pill = State()
    new_time = State()
    remove_time = State()
    time_to_add = State()
    time_to_delete = State()
    approve_delete = State()
