import os
import aiogram
import asyncio
import sqlite3

from aiogram import F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import command
from dotenv import load_dotenv


load_dotenv()


TOKEN = os.getenv('BOT_TOKEN')


dispatcher = aiogram.Dispatcher()


@dispatcher.message(command.Command('start'))
async def command_start_handler(message: Message) -> None:

    key = [
        [KeyboardButton(text='Регистрация')]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=key, resize_keyboard=True, input_field_placeholder='Регистрация')

    await message.answer(f'Зарегистрируйтесь пожалуйста!', reply_markup=keyboard)


@dispatcher.message(F.text.lower() == 'регистрация')
async def registration(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    connection = sqlite3.connect('../database/tg_bot.db')
    cursor = connection.cursor()

    cursor.execute(f'SELECT telegram_id FROM users WHERE telegram_id={user_id}')
    if not cursor.fetchone():
        cursor.execute(f'INSERT INTO users (telegram_id, first_name) VALUES ({user_id}, "{user_name}")')
        connection.commit()
        connection.close()
        await message.reply('Вы успешно зарегистрировались', reply_markup=ReplyKeyboardRemove())
    else:
        connection.close()
        await message.reply('Вы уже зарегистрированы в системе!', reply_markup=ReplyKeyboardRemove())


async def main() -> None:
    bot = aiogram.Bot(token=TOKEN)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
