import os
import aiogram

from dotenv import load_dotenv

from aiogram import Bot, types
from aiogram.filters import command

from database import connection as con
from inline_keyboards import get_menu_buttons, get_profile_buttons
from config import config


load_dotenv()


bot = Bot(token=config.BOT_TOKEN)

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

    markup = get_menu_buttons()

    text = 'Вы находитесь в главном меню бота - CheFlowers!'
    await message.delete()
    await message.answer(text, reply_markup=markup)


@router.callback_query(lambda call: call.data == 'profile')
async def profile_list(callback_query: types.CallbackQuery):

    await callback_query.answer()
    await callback_query.message.delete()

    markup = get_profile_buttons()

    connection = con.connect_to_postgres()
    cursor = connection.cursor()
    cursor.execute(f'SELECT id FROM users WHERE telegram_id={callback_query.from_user.id}')
    user_id = cursor.fetchone()[0]
    cursor.execute(f'SELECT name, schedule FROM flowers WHERE user_id={user_id}')
    flowers = cursor.fetchall()

    cursor.close()
    connection.close()

    inline_for = f'\n{"-" * 10}\n'.join([f'Название: {data[0]}\nГрафик: Полив {data[1]} раз в неделю' for data in flowers])
    await callback_query.message.answer(text=f'Список ваших цветов: \n{"-" * 10}\n{inline_for}', reply_markup=markup)
