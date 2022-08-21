from aiogram.types import CallbackQuery

from src.database import update_notification_count


async def taken(callback: CallbackQuery):
    time_id = callback.data.split(':')[1]
    await update_notification_count(time_id, 0)

    await callback.bot.send_message(
        callback.from_user.id,
        f'Молодец, что не забыл принять препарат'
    )
    await callback.answer()
