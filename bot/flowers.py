import os
import aiogram

from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from scene import FlowerRegistration
from database import connection
from inline_keyboards import get_menu_buttons


load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))

router = aiogram.Router()


@router.callback_query(lambda call: call.data == 'create_flowers')
async def cmd_flowers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await callback_query.message.delete()
    await callback_query.answer()
    await callback_query.message.answer('Введите название цветка!')
    await state.set_state(FlowerRegistration.name)


@router.message(FlowerRegistration.name)
async def process_flower_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer('Введите количество дней в неделю, которое необходимо для полива растения!')
    await state.set_state(FlowerRegistration.graph)


@router.message(FlowerRegistration.graph)
async def process_flower_graph(message: types.Message, state: FSMContext) -> None:
    await state.update_data(graph=message.text)

    data = await state.get_data()

    conn = connection.connect_to_postgres()
    cursor = conn.cursor()

    cursor.execute(f'SELECT id FROM users WHERE telegram_id={message.from_user.id}')
    user_id = cursor.fetchone()[0]

    query = 'INSERT INTO flowers (name, user_id, schedule) VALUES(%s, %s, %s)'
    insert_data = (data['name'], user_id, data['graph'])
    cursor.execute(query, insert_data)

    conn.commit()

    cursor.close()
    conn.close()

    message_data = f'''Данные успешно сохранены, вы ввели:
Название цветка - {data["name"]}
График - {data["graph"]}'''

    markup = get_menu_buttons()

    await message.answer(message_data, reply_markup=markup)
    await state.clear()
