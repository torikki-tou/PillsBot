import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher.filters.builtin import CommandStart, Text

from src import handlers
from src.keyboard import Button
from src.states import NewPill, Info, RenamePill, AddTime, DeleteTime, DeletePill


bot = Bot(os.environ.get('BOT_TOKEN'))
storage = RedisStorage2(host='redis')
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
    handlers.pills.rename.input_, Text(Button.rename_pill.value), state=Info.update)
dispatcher.register_message_handler(
    handlers.pills.rename.save, state=RenamePill.title)

dispatcher.register_message_handler(
    handlers.pills.time.add.input_, Text(Button.add_time.value), state=Info.update)
dispatcher.register_message_handler(
    handlers.pills.time.add.save, state=AddTime.time)

dispatcher.register_message_handler(
    handlers.pills.time.delete.choose, Text(Button.delete_time.value), state=Info.update)
dispatcher.register_message_handler(
    handlers.pills.time.delete.perform, state=DeleteTime.time)

dispatcher.register_message_handler(
    handlers.pills.notifications.switch, Text([Button.pill_on.value, Button.pill_off.value]), state=Info.update)

dispatcher.register_message_handler(
    handlers.pills.delete.ask_for_approve, Text(Button.delete_pill.value), state=Info.update)
dispatcher.register_message_handler(
    handlers.pills.delete.perform, Text(Button.delete_pill.value), state=DeletePill.approve)

dispatcher.register_message_handler(
    handlers.pills.core.unknown_message,  state='*')

