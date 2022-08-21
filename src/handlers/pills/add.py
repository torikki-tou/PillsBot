from datetime import datetime

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from src.database import insert_new_pill, allowed_to_add_more_pills, insert_times
from src.utils import get_string_from_time
from src.keyboard import Keyboard, Button
from src.states import NewPill


async def start(message: Message):

    if not await allowed_to_add_more_pills(message.from_user.id):
        return await message.answer(
            'Слишком много препаратов, сначала удали что-нибудь',
        )

    await message.answer(
        'Я готов добавить новый препарат, теперь введи название.',
        reply_markup=Keyboard().add_cancel()
    )
    await NewPill.first()


async def title(message: Message, state: FSMContext):
    await state.set_data({'title': message.text, 'taking_times': []})
    await message.answer(
        f'Отлично, я запомнил препарат {message.text}. Теперь введи время в формате, например 08:30.',
        reply_markup=Keyboard().add_cancel()
    )
    await NewPill.next()


async def time(message: Message, state: FSMContext):
    try:
        taking_time = datetime.strptime(message.text, '%H:%M').time().strftime('%H:%M')
    except ValueError:
        return await message.answer('Неправильный формат, перепроверь пожалуйста.')

    state_data = await state.get_data()
    await state.update_data({
        'taking_times': state_data['taking_times'] + [taking_time]
    })
    text = f'Время есть! Теперь добавь ещё одно время, если пьешь {state_data["title"]} больше одного раза в день. ' \
           'Если нет, то сохраняй новое лекарство.'
    await message.answer(
        text,
        reply_markup=Keyboard([[Button.another_time, Button.save_pill]]).add_cancel()
    )
    await NewPill.next()


async def another_time(message: Message, state: FSMContext):
    times = get_string_from_time((await state.get_data())['taking_times'])
    await message.answer(
        text=f'Жду новое время! Уже есть: {times}.',
        reply_markup=Keyboard().add_cancel()
    )
    await NewPill.previous()


async def save(message: Message, state: FSMContext):
    state_data = await state.get_data()

    pill_id = await insert_new_pill(
        message.from_user.id,
        state_data['title'],
    )
    await insert_times(
        pill_id=pill_id,
        times=state_data['taking_times']
    )
    await message.answer(
        f'Препарат {state_data["title"]} сохранен. '
        f'Я буду напоминать тебе принять его в {get_string_from_time(state_data["taking_times"])}.',
        reply_markup=Keyboard().homescreen()
    )
    await state.finish()
