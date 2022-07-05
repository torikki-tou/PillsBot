from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from src.states import Dialog
from src.keyboards import (
    get_homescreen_keyboard,
    get_cancel_keyboard,
    get_all_pills_keyboards,
)


async def start(message: Message):
    await message.answer('hi, i am pills bot', reply_markup=get_homescreen_keyboard())


async def new_pill(message: Message, state: FSMContext):
    await state.set_state(Dialog.new_pill_name)
    await message.answer('waiting for new pill', reply_markup=get_cancel_keyboard())


async def pill_name(message: Message, state: FSMContext):
    await state.set_state(Dialog.new_pill_time)
    await message.answer('now time', reply_markup=get_cancel_keyboard())


async def pill_time(message: Message):
    await message.answer('time set', reply_markup=get_cancel_keyboard())


async def all_pills(message: Message):
    await message.answer('it is all pills', reply_markup=get_all_pills_keyboards())


async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('home screen', reply_markup=get_homescreen_keyboard())
