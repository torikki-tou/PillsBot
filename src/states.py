from aiogram.dispatcher.filters.state import State, StatesGroup


class NewPill(StatesGroup):
    title = State()
    time = State()
    ask_save = State()


class Info(StatesGroup):
    update = State()


class RenamePill(StatesGroup):
    title = State()


class AddTime(StatesGroup):
    time = State()


class DeleteTime(StatesGroup):
    time = State()


class DeletePill(StatesGroup):
    approve = State()
