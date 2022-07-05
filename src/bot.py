import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.builtin import CommandStart

from src.handlers import (
    start,
    new_pill,
    all_pills,
    pill_name,
    pill_time,
    cancel
)
from src.states import Dialog

bot = Bot(os.environ.get('BOT_TOKEN'))
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)


dispatcher.register_message_handler(start, CommandStart())
dispatcher.register_message_handler(cancel, lambda message: message.text == 'cancel', state='*')
dispatcher.register_message_handler(new_pill, lambda message: message.text == 'new', state=None)
dispatcher.register_message_handler(all_pills, lambda message: message.text == 'all', state=None)
dispatcher.register_message_handler(pill_name, state=Dialog.new_pill_name)
dispatcher.register_message_handler(pill_time, state=Dialog.new_pill_time)
