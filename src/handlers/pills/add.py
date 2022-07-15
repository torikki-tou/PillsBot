from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from src.database import insert_new_pill
from src.keyboards import get_cancel_keyboard, get_save_pill_keyboards, get_homescreen_keyboard
from src.states import Dialog
from src.utils import get_string_from_time


async def start(message: Message, state: FSMContext):
    await state.set_state(Dialog.new_pill_title)
    await state.set_data(None)
    await message.answer(
        'Я готов добавить новый препарат, теперь введи название.',
        reply_markup=await get_cancel_keyboard()
    )


async def title(message: Message, state: FSMContext):
    await state.set_state(Dialog.new_pill_time)
    await state.set_data({'title': message.text, 'time': []})
    text = f'Отлично, я запомнил препарат {message.text}. Теперь введи время в формате, например 08:30'
    await message.answer(text, reply_markup=await get_cancel_keyboard())


async def time(message: Message, state: FSMContext):
    try:
        time_str = datetime.strptime(message.text, '%H:%M').time().strftime('%H:%M')
    except ValueError:
        return await message.answer('Неправильный формат, перепроверь пожалуйста.')

    await state.set_state(Dialog.new_pill_save)
    state_data = await state.get_data()
    await state.update_data({
        'time': state_data['time'] + [time_str]
    })
    text = f'Время есть! Теперь добавь ещё одно время, если пьешь {state_data["title"]} больше одного раза в день. ' \
           'Если нет, то сохраняй новое лекарство.'
    await message.answer(text, reply_markup=await get_save_pill_keyboards())


async def another_time(message: Message, state: FSMContext):
    await state.set_state(Dialog.new_pill_time)
    state_data = await state.get_data()
    text = f'Жду новое время! Уже есть: {await get_string_from_time(state_data["time"])}'
    await message.answer(text, reply_markup=await get_cancel_keyboard())


async def save(message: Message, state: FSMContext):
    state_data = await state.get_data()
    await insert_new_pill(message.from_user.id, state_data['title'], state_data["time"])
    time_str = await get_string_from_time(state_data["time"])
    text = f'Препарат {state_data["title"]} сохранен. Я буду напоминать тебе принять его в {time_str}'
    await state.finish()
    await state.set_data()
    await message.answer(text, reply_markup=await get_homescreen_keyboard())
