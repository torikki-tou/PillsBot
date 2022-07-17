from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from src.states import DeleteTime
from src.keyboard import Keyboard
from src.database import delete_pill_time


async def choose(message: Message, state: FSMContext):
    await message.answer(
        'Выбери, какое время удалить',
        reply_markup=Keyboard([(await state.get_data())['times_to_take']], row_width=5).add_cancel()
    )
    await DeleteTime.first()


async def perform(message: Message, state: FSMContext):
    try:
        time_str = datetime.strptime(message.text, '%H:%M').time().strftime('%H:%M')
    except ValueError:
        return await message.answer('Неправильный формат, перепроверь пожалуйста.')

    if time_str not in (await state.get_data())['times_to_take']:
        return await message.answer('Такого времени нету.')

    await delete_pill_time((await state.get_data())['_id'], message.text)
    await message.answer('Время удалено', reply_markup=Keyboard().homescreen())
    await state.finish()
