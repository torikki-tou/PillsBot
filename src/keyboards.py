from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)


def get_homescreen_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton('Новая таблетка'), KeyboardButton('Все таблетки')]],
        resize_keyboard=True
    )


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton('На главную')]],
        resize_keyboard=True
    )


def get_all_pills_keyboards() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(1)
    keyboard.add(
        InlineKeyboardButton('first pill', callback_data='1'),
        InlineKeyboardButton('second pill', callback_data='1')
    )
    return keyboard


def get_save_pill_keyboards() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton('Добавить время'), KeyboardButton('Сохранить')], [KeyboardButton('На главную')]],
        resize_keyboard=True
    )
