import asyncio
import logging
import os


from aiogram import Bot, Dispatcher, types

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from handlers.bad_habits import rt_habits
from handlers.training import rt_train


from data_base.engine import create_db, drop_db, session_maker

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


from handlers.calculator import rt
from common.bot_commands import private


from middlewares.db import DataBaseSession
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aioredis import Redis


token = os.getenv("TOKEN")
bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

logging.basicConfig(level=logging.INFO)

storage = RedisStorage(
        redis=Redis(host="localhost", port=6379),
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True, )
)

dp = Dispatcher(storage=storage)
dp.include_router(rt)
dp.include_router(rt_habits)
dp.include_router(rt_train)


async def on_startup(bot):

    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('бот лег')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

