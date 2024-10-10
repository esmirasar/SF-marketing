import os
import aiogram
import sqlite3

from aiogram import Bot, types
from aiogram.filters import command
from dotenv import load_dotenv


load_dotenv()


TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)

router = aiogram.Router()


@router.message(command.CommandStart())
async def command_start_handler(message: types.Message) -> None:

    button = types.InlineKeyboardButton(text='Зарегистрироваться 🎉', callback_data='registration')
    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.answer(text='Нажмите на кнопку "Зарегистрироваться"', reply_markup=inline_keyboard)


@router.callback_query(lambda text: text.data == 'registration')
async def registration(callback_query: types.CallbackQuery) -> None:
    await callback_query.answer()
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.first_name

    connection = sqlite3.connect('../database/tg_bot.db')
    cursor = connection.cursor()

    cursor.execute(f'SELECT telegram_id FROM users WHERE telegram_id={user_id}')
    if not cursor.fetchone():
        cursor.execute(f'INSERT INTO users (telegram_id, first_name) VALUES ({user_id}, "{user_name}")')
        connection.commit()
        connection.close()
        await bot.send_message(user_id, 'Вы успешно зарегистрировались')
    else:
        connection.close()
        await bot.send_message(user_id, 'Вы уже зарегистрированы в системе!')

