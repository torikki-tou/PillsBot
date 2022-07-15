from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from src.keyboards import get_cancel_keyboard


async def input_(message: Message, state: FSMContext):
    await state.set_state()
    await message.answer('Введи новое название', reply_markup=await get_cancel_keyboard())


async def save(message: Message, state: FSMContext):
    pill_id = (await state.get_data())['pill_id']

