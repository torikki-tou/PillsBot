from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from src.keyboard import Keyboard


async def input_(message: Message, state: FSMContext):
    await state.set_state()
    await message.answer('Введи новое название', reply_markup=Keyboard().add_cancel())


async def save(message: Message, state: FSMContext):
    pill_id = (await state.get_data())['pill_id']

