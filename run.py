import logging

from aiogram import executor

from src.bot import dispatcher

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
