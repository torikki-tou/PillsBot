from datetime import datetime

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from src.states import Dialog
from src.keyboards import (
    get_homescreen_keyboard,
    get_cancel_keyboard,
    get_all_pills_keyboards,
    get_save_pill_keyboards,
    get_pill_info_keyboard,
    get_delete_approve_keyboard
)
from src.database import (
    insert_new_user,
    insert_new_pill,
    get_pill_by_id,
    get_all_pills_of_user,
    delete_pill
)
from src.utils import get_string_from_time


async def start(message: Message):
    await insert_new_user(message.from_user)
    text = 'Привет! Я таблеточный бот, помогу тебе выпить таблетки вовремя и не получить по жопе. ' \
           'Теперь можешь начать добавлять таблетки!'
    await message.answer(text, reply_markup=await get_homescreen_keyboard())


async def new_pill(message: Message, state: FSMContext):
    await state.set_state(Dialog.new_pill_title)
    await state.set_data(None)
    await message.answer(
        'Я готов добавить новый препарат, теперь введи название.',
        reply_markup=await get_cancel_keyboard()
    )


async def pill_title(message: Message, state: FSMContext):
    await state.set_state(Dialog.new_pill_time)
    await state.set_data({'title': message.text, 'time': []})
    text = f'Отлично, я запомнил препарат {message.text}. Теперь введи время в формате, например 08:30'
    await message.answer(text, reply_markup=await get_cancel_keyboard())


async def pill_time(message: Message, state: FSMContext):
    try:
        time = datetime.strptime(message.text, '%H:%M').time().strftime('%H:%M')
    except ValueError:
        return await message.answer('Неправильный формат, перепроверь пожалуйста.')

    await state.set_state(Dialog.new_pill_save)
    state_data = await state.get_data()
    await state.update_data({
        'time': state_data['time'] + [time]
    })
    text = f'Время есть! Теперь добавь ещё одно время, если пьешь {state_data["title"]} больше одного раза в день. ' \
           'Если нет, то сохраняй новое лекарство.'
    await message.answer(text, reply_markup=await get_save_pill_keyboards())


async def pill_another_time(message: Message, state: FSMContext):
    await state.set_state(Dialog.new_pill_time)
    state_data = await state.get_data()
    text = f'Жду новое время! Уже есть: {await get_string_from_time(state_data["time"])}'
    await message.answer(text, reply_markup=await get_cancel_keyboard())


async def pill_saved(message: Message, state: FSMContext):
    state_data = await state.get_data()
    await insert_new_pill(message.from_user.id, state_data['title'], state_data["time"])
    time_str = await get_string_from_time(state_data["time"])
    text = f'Препарат {state_data["title"]} сохранен. Я буду напоминать тебе принять его в {time_str}'
    await state.finish()
    await state.set_data()
    await message.answer(text, reply_markup=await get_homescreen_keyboard())


async def all_pills(message: Message):
    text = 'Вот список всех таблеток, которые ты добавлял. ' \
           'Нажми на препарат, чтобы увидеть или изменить информацию о нем.'
    await message.answer(
        text,
        reply_markup=await get_all_pills_keyboards(
            await get_all_pills_of_user(message.from_user.id)
        )
    )


async def delete_pill_approve(message: Message, state: FSMContext):
    await delete_pill((await state.get_data())['pill_id'])
    await state.finish()
    await state.set_data()
    await message.answer('Препарат удален', reply_markup=await get_homescreen_keyboard())


async def new_pill_title(message: Message, state: FSMContext):
    await state.set_state()
    await message.answer('Введи новое название', reply_markup=await get_cancel_keyboard())


async def rename_pill(message: Message, state: FSMContext):
    pill_id = (await state.get_data())['pill_id']


async def time_to_delete(message: Message, state: FSMContext):
    ...


async def delete_time(message: Message, state: FSMContext):
    ...


async def time_to_add(message: Message, state: FSMContext):
    ...


async def add_time(message: Message, state: FSMContext):
    ...


async def pause_pill(message: Message, state: FSMContext):
    ...


async def ask_delete_pill(message: Message, state: FSMContext):
    await state.set_state(Dialog.approve_delete)
    await message.answer(
        'Точно уверенны, что хотите удалить препарат?',
        reply_markup=await get_delete_approve_keyboard()
    )


async def cancel(message: Message, state: FSMContext):
    if await state.get_state() is None:
        return await message.answer('Ты уже на главной странице.', reply_markup=await get_homescreen_keyboard())
    await state.finish()
    await state.set_data()
    await message.answer(
        'Действие отменено. Ты снова на главной странице.',
        reply_markup=await get_homescreen_keyboard()
    )


async def pill_info_callback(callback: CallbackQuery, state: FSMContext):
    pill_id = callback.data
    pill = await get_pill_by_id(pill_id)
    await state.set_state(Dialog.update_pill)
    await state.set_data({'pill_id': pill_id})
    is_paused = 'Приостановлено' if pill['paused'] else 'Активно'
    text = f'{pill["title"]}\n\n' \
           f'Время приема: {await get_string_from_time(pill["times_to_take"])}\n\n' \
           f'{is_paused}'
    keyboard = await get_pill_info_keyboard()
    await callback.bot.send_message(callback.from_user.id, text, reply_markup=keyboard)
