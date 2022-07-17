from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from src.database import set_notification_status
from src.keyboard import Keyboard


async def switch(message: Message, state: FSMContext):
    await set_notification_status((await state.get_data())['_id'], not (await state.get_data())['paused'])
    text = 'Уведомления включены.' if (await state.get_data())['paused'] else 'Уведомления приостановлены.'
    await message.answer(text, reply_markup=Keyboard().homescreen())
    await state.finish()


