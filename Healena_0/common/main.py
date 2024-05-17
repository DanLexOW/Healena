import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from datetime import datetime, time

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
#load_dotenv('.env')

from handlers.messages import rt
#from handlers.time_code import rt_time
from handlers.group import rt_group
from common.bot_commands import private

from keyboards import reply

token = os.getenv("TOKEN")
bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# parse_mode=ParseMode.HTML

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
dp.include_router(rt)
dp.include_router(rt_group)
#dp.include_router(time_rt)



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет!")




# Запуск процесса поллинга новых апдейтов
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
