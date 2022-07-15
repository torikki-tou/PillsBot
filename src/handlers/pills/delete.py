from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from src.keyboards import get_delete_approve_keyboard, get_homescreen_keyboard
from src.database import delete_pill
from src.states import Dialog


async def ask_for_approve(message: Message, state: FSMContext):
    await state.set_state(Dialog.approve_delete)
    await message.answer(
        'Точно уверенны, что хотите удалить препарат?',
        reply_markup=await get_delete_approve_keyboard()
    )


async def perform(message: Message, state: FSMContext):
    await delete_pill((await state.get_data())['pill_id'])
    await state.finish()
    await state.set_data()
    await message.answer('Препарат удален', reply_markup=await get_homescreen_keyboard())
