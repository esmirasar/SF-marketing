import aiogram

from datetime import datetime, timedelta

from dotenv import load_dotenv

from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from scene import FlowerRegistration
from database import connection
from inline_keyboards import get_menu_buttons, get_profile_buttons
from config import config


load_dotenv()

bot = Bot(token=config.BOT_TOKEN)

router = aiogram.Router()

scheduler = AsyncIOScheduler()
scheduler.start()


@router.callback_query(lambda call: call.data == 'create_flowers')
async def cmd_flowers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await callback_query.message.delete()
    await callback_query.answer()
    await callback_query.message.answer('Какое название у вашего растения?')
    await state.set_state(FlowerRegistration.name)


@router.message(FlowerRegistration.name)
async def process_flower_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer('Через сколько дней необходимо поливать растение?')
    await state.set_state(FlowerRegistration.graph)


@router.message(FlowerRegistration.graph)
async def process_flower_graph(message: types.Message, state: FSMContext) -> None:
    markup_end = get_menu_buttons()
    markup_exception = get_profile_buttons()

    await state.update_data(graph=message.text)

    data = await state.get_data()

    try:
        if int(data['graph']) not in range(1, 8):
            await message.answer(
                text='Бот на данный момент может уведомлять ежедневно, то есть необходимо указать количество дней в диапазоне от 1 до 7 включительно',
                reply_markup=markup_exception
            )
            return None
    except Exception as e:
        print(f'{message.from_user.id} - {e}')
        await message.answer(
            text='Вы ввели не правильное число дней!',
            reply_markup=markup_exception
        )
        return None

    conn = connection.connect_to_postgres()
    cursor = conn.cursor()

    cursor.execute(f'SELECT id FROM users WHERE telegram_id={message.from_user.id}')
    user_id = cursor.fetchone()[0]

    query = 'INSERT INTO flowers (name, user_id, schedule) VALUES(%s, %s, %s)'
    insert_data = (data['name'].title(), user_id, data['graph'])

    try:
        cursor.execute(query, insert_data)
    except Exception as e:
        print(f'{message.from_user.id} - {e}')
        await message.answer(
            text='Вы ввели имя растений, которое уже было добавлено или неверно указали время полива.',
            reply_markup=markup_exception
        )
        cursor.close()
        conn.close()
        return None

    conn.commit()

    cursor.close()
    conn.close()

    message_data = f'''Полив для растения «{data["name"]}» каждый {data["graph"]}-й день.
Вам придёт уведомление - {(datetime.today() + timedelta(days=int(data["graph"]))).strftime("%d.%m.%y в 08:00 утра")}'''

    await message.answer(message_data, reply_markup=markup_end)
    await state.clear()

    scheduler.add_job(
        func=flowers_message,
        trigger=CronTrigger(day=f'*/{data["graph"]}', hour=8, minute=0),
        kwargs={'chat_id': message.chat.id, 'flower_name': data['name']})


async def flowers_message(chat_id: int, flower_name: str):
    await bot.send_message(chat_id=chat_id, text=f'Доброе утро, вам необходимо полить цветок - {flower_name}')
