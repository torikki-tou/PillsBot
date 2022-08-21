from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot import dispatcher
from src.database import (
    get_times_to_notify,
    update_notification_count,
    get_pill_by_id,
    reset_notification_count
)


async def notify():
    async for time in await get_times_to_notify(datetime.now().time().strftime('%H:%M')):
        pill = await get_pill_by_id(time['pill_id'])
        await update_notification_count(time['_id'], time['notifications'] - 1)
        await dispatcher.bot.send_message(
            pill['user_id'],
            f'Тебе пора пить {pill["title"]}',
            reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                'Выпил',
                callback_data=f'notification:{str(time["_id"])}'
            ))
        )


async def reset():
    await notify()
    await reset_notification_count()
