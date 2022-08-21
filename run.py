import os
import asyncio
from datetime import time, timezone, timedelta
import logging

from aiogram.utils.executor import start_polling, start_webhook
import aioschedule

from src.bot import dispatcher
from src.tasks import notify, reset

logging.basicConfig(level=logging.INFO)

TZ = timezone(timedelta(hours=int(os.environ.get('TZ'))))


async def background_tasks():
    aioschedule.every(5).minutes.do(notify)
    aioschedule.every().day.at(time(hour=0, tzinfo=TZ).strftime('%H:%M')).do(reset)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp):
    asyncio.create_task(background_tasks())
    if not int(os.environ.get('DEBUG')):
        await dp.bot.set_webhook(os.environ.get('WEBHOOK_URL'))


async def on_shutdown(dp):
    if not int(os.environ.get('DEBUG')):
        await dp.bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    if int(os.environ.get('DEBUG')):
        start_polling(
            dispatcher=dispatcher,
            skip_updates=True,
            reset_webhook=True,
            on_startup=on_startup
        )
    else:
        start_webhook(
            dispatcher=dispatcher,
            webhook_path='/webhook',
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            port='8000'
        )
