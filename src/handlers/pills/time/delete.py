from datetime import datetime

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from src.database import delete_times, get_times_of_pill
from src.keyboard import Keyboard
from src.states import DeleteTime


async def choose(message: Message, state: FSMContext):
    times = [time['time'] for time in await get_times_of_pill((await state.get_data())['_id'])]
    await message.answer(
        'Выбери, какое время хочешь удалить.',
        reply_markup=Keyboard([times], row_width=5).add_cancel()
    )
    await DeleteTime.first()


async def perform(message: Message, state: FSMContext):
    try:
        taking_time = datetime.strptime(message.text, '%H:%M').time().strftime('%H:%M')
    except ValueError:
        return await message.answer('Неправильный формат, перепроверь пожалуйста.')

    times = [time['time'] for time in await get_times_of_pill((await state.get_data())['_id'])]
    if taking_time not in times:
        return await message.answer('Такого времени нету.')

    await delete_times(
        pill_id=(await state.get_data())['_id'],
        time=taking_time
    )
    await message.answer('Время удалено.', reply_markup=Keyboard().homescreen())
    await state.finish()
