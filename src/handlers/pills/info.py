from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.database import get_pills_of_user, get_pill_by_id, get_times_of_pill
from src.utils import get_string_from_time
from src.keyboard import Keyboard, Button
from src.states import Info


async def all_(message: Message):
    pills = await get_pills_of_user(message.from_user.id)
    if not pills:
        return await message.answer('У тебя пока нет ни одной таблетки.', reply_markup=Keyboard().homescreen())

    text = 'Вот список всех таблеток, которые ты добавлял. ' \
           'Нажми на препарат, чтобы увидеть или изменить информацию о нем.'
    keyboard = InlineKeyboardMarkup(1)
    for pill in pills:
        keyboard.add(InlineKeyboardButton(pill['title'], callback_data=f'pill:{str(pill["_id"])}'))
    await message.answer(text, reply_markup=keyboard)


async def by_id(callback: CallbackQuery, state: FSMContext):
    pill = await get_pill_by_id(callback.data.split(':')[1])
    if not pill:
        return await callback.answer('Я не знаю эту таблетку')

    await state.set_data({**pill, '_id': str(pill['_id'])})

    taking_times = [time['time'] for time in await get_times_of_pill(pill['_id'])]
    text = f'*{pill["title"]}\n\n*' \
           f'Принимать в {get_string_from_time(taking_times)}\n\n' \
           f'Уведомления: {"выключены" if pill["paused"] else "включены"}'

    await callback.bot.send_message(
        callback.from_user.id, text,
        parse_mode='MarkdownV2',
        reply_markup=Keyboard([
            [Button.rename_pill],
            [Button.add_time, Button.delete_time],
            [Button.pill_on if pill['paused'] else Button.pill_off, Button.delete_pill]
        ]).add_cancel()
    )
    await Info.first()
    await callback.answer()
