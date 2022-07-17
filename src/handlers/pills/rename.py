from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from src.keyboard import Keyboard
from src.states import RenamePill
from src.database import update_pill_title


async def input_(message: Message):
    await message.answer('Введи новое название.', reply_markup=Keyboard().add_cancel())
    await RenamePill.first()


async def save(message: Message, state: FSMContext):
    if message.text == (await state.get_data())['title']:
        await message.answer('Препарат уже так называется. '
                             'Если не хочешь менять название, просто нажми "На главную".')

    await update_pill_title((await state.get_data())['_id'], message.text)
    await message.answer(
        f'Название было изменено с {(await state.get_data())["title"]} на {message.text}.',
        reply_markup=Keyboard().homescreen()
    )
    await state.finish()

