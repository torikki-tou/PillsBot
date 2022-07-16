from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from src.keyboards import get_all_pills_keyboards
from src.keyboard import Keyboard, Button
from src.database import get_all_pills_of_user, get_pill_by_id
from src.states import Info
from src.utils import get_string_from_time


async def all_(message: Message):
    text = 'Вот список всех таблеток, которые ты добавлял. ' \
           'Нажми на препарат, чтобы увидеть или изменить информацию о нем.'
    await message.answer(
        text,
        reply_markup=await get_all_pills_keyboards(
            await get_all_pills_of_user(message.from_user.id)
        )
    )


async def by_id(callback: CallbackQuery, state: FSMContext):
    pill_id = callback.data
    pill = await get_pill_by_id(pill_id)
    await Info.first()
    await state.set_data({'pill_id': pill_id})
    text = f'{pill["title"]}\n\n' \
           f'Время приема: {await get_string_from_time(pill["times_to_take"])}\n\n' \
           f'{"Приостановлено" if pill["paused"] else "Активно"}'
    await callback.bot.send_message(
        callback.from_user.id, text,
        reply_markup=Keyboard([
            [Button.rename_pill],
            [Button.add_time, Button.delete_time],
            [Button.pause, Button.delete_pill]
        ]).add_cancel()
    )
