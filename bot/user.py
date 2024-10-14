import os
import aiogram

from aiogram import Bot, types
from aiogram.filters import command
from dotenv import load_dotenv

from database import connection as con


load_dotenv()


TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)

router = aiogram.Router()


@router.message(command.Command('start'))
async def command_start_handler(message: types.Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    connection = con.connect_to_postgres()
    cursor = connection.cursor()

    cursor.execute(f'SELECT telegram_id FROM users WHERE telegram_id={user_id}')
    if not cursor.fetchone():
        insert_query = 'INSERT INTO users (telegram_id, first_name) VALUES (%s, %s);'
        insert_data = (user_id, user_name)

        cursor.execute(insert_query, insert_data)

        connection.commit()
        connection.close()

    text = '''Добро пожаловать в CheFlowers
Я предназначен для напоминания вам о ваших цветах
Введите пожалуйста команду /flowers для продолжения'''

    await message.reply(text)
