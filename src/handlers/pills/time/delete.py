from aiogram.dispatcher import FSMContext
from aiogram.types import Message


async def choose(message: Message, state: FSMContext):
    ...


async def perform(message: Message, state: FSMContext):
    ...

