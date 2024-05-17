import asyncio
import logging
import os
import aioschedule
from aiogram import F, Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
from data_base.engine import create_db, drop_db, session_maker

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from threading import Thread

from aiogram.handlers import callback_query, message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers import apched
from aiogram.filters.command import Command

from handlers.messages import rt
from handlers.group import rt_group
from common.bot_commands import private

from datetime import datetime, timedelta

from middlewares.db import DataBaseSession
#load_dotenv('.env')
#from data_base.engine import create_db


from keyboards import reply

token = os.getenv("TOKEN")
bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# parse_mode=ParseMode.HTML

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(rt)
dp.include_router(rt_group)

'''@dp.message(Command("music"))
async def time(message: types.Message):
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(apched.send_message_time, trigger='date', run_date=datetime.now() + timedelta(seconds=10),
                      kwargs={'message_id': message.from_user.id})
    scheduler.start()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


@dp.message_handler(func=lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')'''

# Запуск процесса поллинга новых апдейтов

'''async def on_startup(bot):

    # await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('бот лег')'''


'''async def noon_print():
    print("It's noon!")

async def scheduler():
    aioschedule.every().day.at("10:26").do(noon_print)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())'''


async def on_startup(bot):

    run_param = False
    if run_param:
        await drop_db() #+импортируем

    await create_db()


async def on_shutdown(bot):
    print('бот лег')


async def main():
    dp.startup.register(on_startup)  # чтобы работало во время старта/завершения бота
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    
    await create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

