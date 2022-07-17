from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from src.database import insert_new_pill
from src.keyboard import Keyboard, Button
from src.states import NewPill
from src.utils import get_string_from_time


async def start(message: Message):
    await message.answer(
        'Я готов добавить новый препарат, теперь введи название.',
        reply_markup=Keyboard().add_cancel()
    )
    await NewPill.first()


async def title(message: Message, state: FSMContext):
    await state.set_data({'title': message.text, 'time': []})
    text = f'Отлично, я запомнил препарат {message.text}. Теперь введи время в формате, например 08:30.'
    await message.answer(text, reply_markup=Keyboard().add_cancel())
    await NewPill.next()


async def time(message: Message, state: FSMContext):
    try:
        time_str = datetime.strptime(message.text, '%H:%M').time().strftime('%H:%M')
    except ValueError:
        return await message.answer('Неправильный формат, перепроверь пожалуйста.')

    state_data = await state.get_data()
    await state.update_data({
        'time': state_data['time'] + [time_str]
    })
    text = f'Время есть! Теперь добавь ещё одно время, если пьешь {state_data["title"]} больше одного раза в день. ' \
           'Если нет, то сохраняй новое лекарство.'
    await message.answer(text, reply_markup=Keyboard([[Button.another_time, Button.save_pill]]).add_cancel())
    await NewPill.next()


async def another_time(message: Message, state: FSMContext):
    state_data = await state.get_data()
    text = f'Жду новое время! Уже есть: {await get_string_from_time(state_data["time"])}.'
    await message.answer(text, reply_markup=Keyboard().add_cancel())
    await NewPill.previous()


async def save(message: Message, state: FSMContext):
    state_data = await state.get_data()
    await insert_new_pill(message.from_user.id, state_data['title'], state_data['time'])
    time_str = await get_string_from_time(state_data['time'])
    text = f'Препарат {state_data["title"]} сохранен. Я буду напоминать тебе принять его в {time_str}.'
    await message.answer(text, reply_markup=Keyboard().homescreen())
    await state.finish()
