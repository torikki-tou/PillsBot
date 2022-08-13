import os
import asyncio
from datetime import time, timezone, timedelta
import logging

from aiogram.utils.executor import start_polling, start_webhook
import aioschedule

from src.bot import dispatcher
from src.tasks import send_notifications, reset

logging.basicConfig(level=logging.INFO)

TZ = timezone(timedelta(hours=int(os.environ.get('TZ'))))


async def background_tasks():
    aioschedule.every().second.do(send_notifications)
    aioschedule.every().day.at(time(hour=0, tzinfo=TZ).strftime('%H:%M')).do(reset)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp):
    await start_background_tasks(None)
    await dp.bot.set_webhook(os.environ.get('WEBHOOK_URL'))


async def on_shutdown(dp):
    await dp.bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()


async def start_background_tasks(_):
    asyncio.create_task(background_tasks())


if __name__ == '__main__':
    if int(os.environ.get('DEBUG')):
        start_polling(
            dispatcher=dispatcher,
            skip_updates=True,
            reset_webhook=True,
            on_startup=start_background_tasks
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
