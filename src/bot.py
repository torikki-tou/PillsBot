import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2 as BustedRedisStorage
from aiogram.dispatcher.filters.builtin import CommandStart

from src.states import Dialog
from src import handlers

bot = Bot(os.environ.get('BOT_TOKEN'))
storage = BustedRedisStorage(host='redis')
dispatcher = Dispatcher(bot, storage=storage)


dispatcher.register_message_handler(
    handlers.pills.core.start, CommandStart())
dispatcher.register_message_handler(
    handlers.pills.core.back_home, lambda message: message.text == 'На главную', state='*')

dispatcher.register_message_handler(
    handlers.pills.add.start, lambda message: message.text == 'Новая таблетка', state=None)
dispatcher.register_message_handler(
    handlers.pills.add.title, state=Dialog.new_pill_title)
dispatcher.register_message_handler(
    handlers.pills.add.time, state=Dialog.new_pill_time)
dispatcher.register_message_handler(
    handlers.pills.add.another_time, lambda message: message.text == 'Добавить время', state=Dialog.new_pill_save)
dispatcher.register_message_handler(
    handlers.pills.add.save, lambda message: message.text == 'Сохранить', state=Dialog.new_pill_save)

dispatcher.register_message_handler(
    handlers.pills.info.all_, lambda message: message.text == 'Все таблетки', state=None)
dispatcher.register_callback_query_handler(
    handlers.pills.info.by_id, state='*')

dispatcher.register_message_handler(
    handlers.pills.rename.input_, lambda message: message.text == 'Удалить', state=Dialog.approve_delete)
dispatcher.register_message_handler(
    handlers.pills.rename.save, lambda message: message.text == 'Удалить', state=Dialog.approve_delete)

# dispatcher.register_message_handler(
#     handlers.pills.time.add.input_, lambda message: message.text == 'Удалить', state=Dialog.approve_delete)
# dispatcher.register_message_handler(
#     handlers.pills.time.add.save, lambda message: message.text == 'Удалить', state=Dialog.approve_delete)
#
# dispatcher.register_message_handler(
#     handlers.pills.time.delete.choose, lambda message: message.text == 'Удалить', state=Dialog.approve_delete)
# dispatcher.register_message_handler(
#     handlers.pills.time.delete.perform, lambda message: message.text == 'Удалить', state=Dialog.approve_delete)
#
# dispatcher.register_message_handler(
#     handlers.pills.pause.perform, lambda message: message.text == 'Удалить', state=Dialog.approve_delete)
#
# dispatcher.register_message_handler(
#     handlers.pills.delete.ask_for_approve, lambda message: message.text == 'Удалить', state=Dialog.approve_delete)
# dispatcher.register_message_handler(
#     handlers.pills.delete.perform, lambda message: message.text == 'Удалить', state=)

dispatcher.register_message_handler(
    handlers.pills.core.unknown_message,  state='*')

