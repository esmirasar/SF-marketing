import os
import asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv


load_dotenv()


bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


async def main():
    import user

    dp.include_router(user.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
