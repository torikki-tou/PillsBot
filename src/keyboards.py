from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)


def get_homescreen_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton('new'), KeyboardButton('all')]],
        resize_keyboard=True
    )


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton('cancel')]],
        resize_keyboard=True
    )


def get_all_pills_keyboards() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(1)
    keyboard.add(
        InlineKeyboardButton('first pill', callback_data='1'),
        InlineKeyboardButton('second pill', callback_data='1')
    )
    return keyboard
