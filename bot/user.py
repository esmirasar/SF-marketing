import os
import aiogram
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv

from aiogram import Bot, types
from aiogram.filters import command
from aiogram.fsm.context import FSMContext

from database import connection as con
from inline_keyboards import get_menu_buttons, get_profile_buttons, get_timezone_buttons
from config import config


load_dotenv()


bot = Bot(token=config.BOT_TOKEN)

router = aiogram.Router()


@router.message(command.Command('start'))
async def command_start_handler(message: types.Message) -> None:

    connection = con.connect_to_postgres()
    cursor = connection.cursor()
    cursor.execute(f'SELECT telegram_id FROM users WHERE telegram_id={message.from_user.id}')

    if cursor.fetchone():
        connection.close()
        cursor.close()
        text = 'Вы находитесь в главном меню бота - CheFlowers!'
        await message.answer(text=text, reply_markup=get_menu_buttons())
    else:
        text = 'Введите ваш часовой пояс в формате UTC±HH:MM. Например UTC+3:00.'
        await message.answer(text=text, reply_markup=get_timezone_buttons())


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

    if flowers:
        inline_for = f'\n{"-" * 10}\n'.join([f'Название: {data[0]}\nГрафик: Полив каждый {data[1]}-й день' for data in flowers])
        await callback_query.message.answer(text=f'Список ваших цветов: \n{"-" * 10}\n{inline_for}', reply_markup=markup)
    else:
        await callback_query.message.answer(text='В вашем профиле растений нет!', reply_markup=markup)


@router.callback_query(lambda call: call.data[1:].isdigit() if call.data.startswith('-') else call.data.isdigit())
async def utc_function(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.first_name

    connection = con.connect_to_postgres()
    cursor = connection.cursor()

    cursor.execute(f'SELECT telegram_id FROM users WHERE telegram_id={user_id}')
    if not cursor.fetchone():
        insert_query = 'INSERT INTO users (telegram_id, first_name, time_zone) VALUES (%s, %s, %s);'
        insert_data = (user_id, user_name, callback_query.data)

        cursor.execute(insert_query, insert_data)

        connection.commit()
        connection.close()

    markup = get_menu_buttons()

    text = 'Вы находитесь в главном меню бота - CheFlowers!'
    await callback_query.message.delete()
    await callback_query.message.answer(text, reply_markup=markup)
