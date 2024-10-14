import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv


load_dotenv()


bot = Bot(token=os.getenv('BOT_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def main():
    import user
    import flowers

    dp.include_router(user.router)
    dp.include_router(flowers.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
