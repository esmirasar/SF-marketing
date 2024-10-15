from aiogram import types


def get_menu_buttons():

    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Профиль', callback_data='profile')],
    ])

    return markup


def get_profile_buttons():

    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Создание записи', callback_data='create_flowers')]
    ])

    return markup
