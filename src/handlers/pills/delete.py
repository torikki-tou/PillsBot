from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from src.database import delete_pill, delete_times
from src.keyboard import Keyboard, Button
from src.states import DeletePill


async def ask_for_approve(message: Message):
    await message.answer(
        'Точно уверенны, что хотите удалить препарат?',
        reply_markup=Keyboard([[Button.approve_delete_pill]]).add_cancel()
    )
    await DeletePill.first()


async def perform(message: Message, state: FSMContext):
    pill_id = (await state.get_data())['_id']
    await delete_pill(pill_id)
    await delete_times(pill_id)
    await message.answer('Препарат удален.', reply_markup=Keyboard().homescreen())
    await state.finish()
