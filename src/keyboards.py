from typing import AsyncIterable

from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)


async def get_homescreen_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton('Новая таблетка'), KeyboardButton('Все таблетки')]],
        resize_keyboard=True
    )


async def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton('На главную')]],
        resize_keyboard=True
    )


async def get_all_pills_keyboards(pills: AsyncIterable) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(1)
    async for pill in pills:
        keyboard.add(
            InlineKeyboardButton(pill['title'], callback_data='1'),
        )
    return keyboard


async def get_save_pill_keyboards() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton('Добавить время'), KeyboardButton('Сохранить')], [KeyboardButton('На главную')]],
        resize_keyboard=True
    )
