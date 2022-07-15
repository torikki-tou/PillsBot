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
    # TODO: set button limit
    async for pill in pills:
        keyboard.add(
            InlineKeyboardButton(pill['title'], callback_data=str(pill['_id'])),
        )
    return keyboard


async def get_save_pill_keyboards() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton('Добавить время'), KeyboardButton('Сохранить')], [KeyboardButton('На главную')]],
        resize_keyboard=True
    )


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


async def get_delete_approve_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton('Удалить'), KeyboardButton('Отмена')], [KeyboardButton('На главную')]],
        resize_keyboard=True
    )
