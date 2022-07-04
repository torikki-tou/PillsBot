import os

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart

from src.handlers import start

bot = Bot(os.environ.get('TOKEN'))
dp = Dispatcher(bot)


dp.register_message_handler(start, CommandStart)
