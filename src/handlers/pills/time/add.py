from datetime import datetime

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from src.database import add_time_to_pill
from src.keyboard import Keyboard
from src.states import AddTime


async def input_(message: Message):
    await message.answer('Какое время ты хочешь добавить?', reply_markup=Keyboard().add_cancel())
    await AddTime.first()


async def save(message: Message, state: FSMContext):
    try:
        taking_time = datetime.strptime(message.text, '%H:%M').time().strftime('%H:%M')
    except ValueError:
        return await message.answer('Неправильный формат, перепроверь пожалуйста.')

    await add_time_to_pill((await state.get_data())['_id'], taking_time)
    await message.answer('Новое время сохранено.', reply_markup=Keyboard().homescreen())
    await state.finish()
