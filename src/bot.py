import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2 as BustedRedisStorage
from aiogram.dispatcher.filters.builtin import CommandStart

from src.handlers import (
    start,
    new_pill,
    all_pills,
    pill_title,
    pill_time,
    pill_another_time,
    pill_saved,
    cancel
)
from src.states import Dialog

bot = Bot(os.environ.get('BOT_TOKEN'))
storage = BustedRedisStorage(host='redis')
dispatcher = Dispatcher(bot, storage=storage)


dispatcher.register_message_handler(start, CommandStart())
dispatcher.register_message_handler(cancel, lambda message: message.text == 'На главную', state='*')
dispatcher.register_message_handler(new_pill, lambda message: message.text == 'Новая таблетка', state=None)
dispatcher.register_message_handler(all_pills, lambda message: message.text == 'Все таблетки', state=None)
dispatcher.register_message_handler(pill_title, state=Dialog.new_pill_title)
dispatcher.register_message_handler(pill_time, state=Dialog.new_pill_time)
dispatcher.register_message_handler(
    pill_another_time,
    lambda message: message.text == 'Добавить время',
    state=Dialog.new_pill_save
)
dispatcher.register_message_handler(
    pill_saved,
    lambda message: message.text == 'Сохранить',
    state=Dialog.new_pill_save
)
