from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


home_button = InlineKeyboardButton(text='🏠 В главное меню', callback_data='home')


def home_kb():
    keyboard = InlineKeyboardMarkup(row_width=1).add(home_button)
    return keyboard


def static_kb():
    static_button = InlineKeyboardButton(text='Статистика', callback_data='static')
    keyboard = InlineKeyboardMarkup(row_width=1).add(static_button)
    return keyboard


def operations_kb():
    plus_button = InlineKeyboardButton(text='+', callback_data='sign:+')
    minus_button = InlineKeyboardButton(text='-', callback_data='sign:-')
    multiply_button = InlineKeyboardButton(text='*', callback_data='sign:*')
    divide_button = InlineKeyboardButton(text='/', callback_data='sign:/')
    keyboard = InlineKeyboardMarkup(row_width=4).add(plus_button, minus_button, multiply_button, divide_button,
                                                     home_button)
    return keyboard
