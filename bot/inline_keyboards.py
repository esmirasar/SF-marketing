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


def get_timezone_buttons():

    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='UTC+2:00 (Калининград)', callback_data='-1'),
         types.InlineKeyboardButton(text='UTC+3:00 (Москва)', callback_data='0'),
         types.InlineKeyboardButton(text='UTC+4:00 (Самара)', callback_data='1')],
        [types.InlineKeyboardButton(text='UTC+5:00 (Екатеринбург)', callback_data='2'),
         types.InlineKeyboardButton(text='UTC+6:00 (Омск)', callback_data='3'),
         types.InlineKeyboardButton(text='UTC+7:00 (Красноярск)', callback_data='4')],
        [types.InlineKeyboardButton(text='UTC+8:00 (Иркутск)', callback_data='5'),
         types.InlineKeyboardButton(text='UTC+9:00 (Якутск)', callback_data='6'),
         types.InlineKeyboardButton(text='UTC+10:00 (Владивосток)', callback_data='7')],
        [types.InlineKeyboardButton(text='UTC+11:00 (Магадан)', callback_data='8'),
         types.InlineKeyboardButton(text='UTC+12:00 (Камчатка)', callback_data='9'),
         types.InlineKeyboardButton(text='UTC+13:00 (Анадырь)', callback_data='10')]
    ])

    return markup
