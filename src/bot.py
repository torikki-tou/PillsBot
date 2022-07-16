import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2 as BustedRedisStorage
from aiogram.dispatcher.filters.builtin import CommandStart, Text

from src.states import NewPill, Info, RenamePill, AddTime, DeleteTime, DeletePill
from src.keyboard import Button
from src import handlers

bot = Bot(os.environ.get('BOT_TOKEN'))
storage = BustedRedisStorage(host='redis')
dispatcher = Dispatcher(bot, storage=storage)


dispatcher.register_message_handler(
    handlers.pills.core.start, CommandStart())
dispatcher.register_message_handler(
    handlers.pills.core.back_home, Text(Button.cancel.value), state='*')

dispatcher.register_message_handler(
    handlers.pills.add.start, Text(Button.new_pill.value), state=None)
dispatcher.register_message_handler(
    handlers.pills.add.title, state=NewPill.title)
dispatcher.register_message_handler(
    handlers.pills.add.time, state=NewPill.time)
dispatcher.register_message_handler(
    handlers.pills.add.another_time, Text(Button.another_time.value), state=NewPill.ask_save)
dispatcher.register_message_handler(
    handlers.pills.add.save, Text(Button.save_pill.value), state=NewPill.ask_save)

dispatcher.register_message_handler(
    handlers.pills.info.all_, Text(Button.all_pills.value), state=None)
dispatcher.register_callback_query_handler(
    handlers.pills.info.by_id, state=None)

dispatcher.register_message_handler(
    handlers.pills.info.all_, Text(Button.all_pills.value), state=None)

dispatcher.register_message_handler(
    handlers.pills.core.unknown_message,  state='*')

