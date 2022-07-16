from typing import AsyncIterable

from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)


async def get_all_pills_keyboards(pills: AsyncIterable) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(1)
    # TODO: set button limit
    async for pill in pills:
        keyboard.add(
            InlineKeyboardButton(pill['title'], callback_data=str(pill['_id'])),
        )
    return keyboard


async def get_pill_info_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton('Переименовать')],
            [KeyboardButton('Удалить время'), KeyboardButton('Добавить время')],
            [KeyboardButton('Приостановить'), KeyboardButton('Удалить')],
            [KeyboardButton('На главную')]
        ],
        resize_keyboard=True
    )
