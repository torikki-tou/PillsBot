from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from src.database import insert_new_user
from src.keyboards import get_homescreen_keyboard


async def start(message: Message):
    await insert_new_user(message.from_user)
    text = 'Привет! Я таблеточный бот, помогу тебе выпить таблетки вовремя и не получить по жопе. ' \
           'Теперь можешь начать добавлять таблетки!'
    await message.answer(text, reply_markup=await get_homescreen_keyboard())


async def back_home(message: Message, state: FSMContext):
    if await state.get_state() is None:
        return await message.answer('Ты уже на главной странице.', reply_markup=await get_homescreen_keyboard())
    await state.finish()
    await state.set_data()
    await message.answer(
        'Действие отменено. Ты снова на главной странице.',
        reply_markup=await get_homescreen_keyboard()
    )


async def unknown_message(message: Message, state: FSMContext):
    ...

