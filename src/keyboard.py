from enum import Enum

from aiogram.types import ReplyKeyboardMarkup


class Button(str, Enum):
    cancel = 'На главную'
    new_pill = 'Новая таблетка'
    another_time = 'Добавить время'
    save_pill = 'Сохранить'
    all_pills = 'Все таблетки'
    delete_pill = 'Удалить'
    approve_delete_pill = 'Удалить'
    rename_pill = 'Переименовать'
    add_time = 'Добавить время'
    delete_time = 'Удалить время'
    pill_off = 'Выключить'
    pill_on = 'Включить'


class Keyboard(ReplyKeyboardMarkup):
    def __init__(self, *args, **kwargs):
        kwargs['resize_keyboard'] = True
        super(Keyboard, self).__init__(*args, **kwargs)

    def homescreen(self):
        self.row(Button.new_pill, Button.all_pills)
        return self

    def add_cancel(self):
        self.row(Button.cancel)
        return self
