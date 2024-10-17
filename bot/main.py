import asyncio

from aiogram import Bot, Dispatcher, types, utils
from aiogram.fsm.storage.memory import MemoryStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from sqlalchemy import create_engine

from dotenv import load_dotenv

from config import config


load_dotenv()


bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

URI = f'postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'
engine = create_engine(URI)
db_store = {
    'default': SQLAlchemyJobStore(engine=engine, tablename='flower_schedulers')
}
scheduler = AsyncIOScheduler(jobstores=db_store)
scheduler.start()


async def set_bot_commands(tg_bot: Bot):
    commands = [
        types.BotCommand(command='/start', description='Начать работу с ботом')
    ]
    await tg_bot.set_my_commands(commands)


async def on_startup(dispatcher: Dispatcher):
    await set_bot_commands(bot)

    for job in scheduler.get_jobs():
        job.resume()


async def main():
    import user
    import flowers

    dp.include_router(user.router)
    dp.include_router(flowers.router)
    await on_startup(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
