import os
import aiogram
import sqlite3

from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.filters.command import Command, CommandObject

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))

router = aiogram.Router()


@router.message(Command("flowers"))
async def cmd_flowers(message: types.Message, command: CommandObject) -> None:
    args = command.args.split()
    if len(args) == 2:
        name, schedule = command.args.split()

        connection = sqlite3.connect('../database/tg_bot.db')
        cursor = connection.cursor()
        cursor.execute(f'SELECT id FROM users WHERE telegram_id={message.from_user.id}')
        user_id = cursor.fetchone()[0]
        try:
            cursor.execute(f'INSERT INTO flowers (name, user_id, schedule) VALUES ("{name}", {user_id}, {schedule})')

            connection.commit()
            connection.close()

            await message.answer(f'Цветок сохранен')
        except Exception as e:
            await message.answer(f'Кажется Вы ввели некорректные данные!')
    else:
        await message.answer(f'Кажется Вы ввели некорректные данные!')


