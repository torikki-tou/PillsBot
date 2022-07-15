from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from src.keyboards import get_all_pills_keyboards, get_pill_info_keyboard
from src.database import get_all_pills_of_user, get_pill_by_id
from src.states import Dialog
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
    await state.set_state(Dialog.update_pill)
    await state.set_data({'pill_id': pill_id})
    is_paused = 'Приостановлено' if pill['paused'] else 'Активно'
    text = f'{pill["title"]}\n\n' \
           f'Время приема: {await get_string_from_time(pill["times_to_take"])}\n\n' \
           f'{is_paused}'
    keyboard = await get_pill_info_keyboard()
    await callback.bot.send_message(callback.from_user.id, text, reply_markup=keyboard)
