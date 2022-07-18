from datetime import datetime

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from src.database import delete_pill_time
from src.keyboard import Keyboard
from src.states import DeleteTime


async def choose(message: Message, state: FSMContext):
    await message.answer(
        'Выбери, какое время хочешь удалить.',
        reply_markup=Keyboard([(await state.get_data())['taking_times']], row_width=5).add_cancel()
    )
    await DeleteTime.first()


async def perform(message: Message, state: FSMContext):
    try:
        taking_time = datetime.strptime(message.text, '%H:%M').time().strftime('%H:%M')
    except ValueError:
        return await message.answer('Неправильный формат, перепроверь пожалуйста.')

    if taking_time not in (await state.get_data())['taking_times']:
        return await message.answer('Такого времени нету.')

    await delete_pill_time((await state.get_data())['_id'], taking_time)
    await message.answer('Время удалено.', reply_markup=Keyboard().homescreen())
    await state.finish()
