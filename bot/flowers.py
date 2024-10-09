import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))

dp = Dispatcher()


@dp.message(Command("flowers"))
async def cmd_flowers(message: types.Message) -> None:
    await message.answer("Растение сохранено")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())