import os
import asyncio
import aiogram

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))

router = aiogram.Router()


@router.message(Command("flowers"))
async def cmd_flowers(message: types.Message, command: CommandObject) -> None:
    name, schedule = command.args.split()

    await message.answer(f'Введите цветок')


