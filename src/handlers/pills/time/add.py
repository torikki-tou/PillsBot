from aiogram.dispatcher import FSMContext
from aiogram.types import Message


async def input_(message: Message, state: FSMContext):
    ...


async def save(message: Message, state: FSMContext):
    ...
