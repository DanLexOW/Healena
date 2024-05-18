import aiocron
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import logging

from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


from data_base.orm_query import orm_get_ids, orm_update_id
from main import storage

from aiogram.fsm.storage.base import StorageKey


token = '7142739750:AAGyfmowTD29-ZcllG_13JGdMDoDJ3HCbIE'
bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(storage=storage)


DB_URL = "sqlite+aiosqlite:////Users/maccount/PycharmProjects/python/Healena_project/my_base.db"
engine = create_async_engine(DB_URL, echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@aiocron.crontab('0 0 * * *')
async def hi():
    async with session_maker() as session:
        for user_date in await orm_get_ids(session):
            if user_date.send == "Да":
                state_with: FSMContext = FSMContext(
                    storage=dp.storage,
                    key=StorageKey(
                        chat_id=user_date.user_id,
                        user_id=user_date.user_id,
                        bot_id=bot.id))
                user_data = user_date.calc_data
                if not (user_data == "ничего пока нет"):
                    user_data = user_data.split()
                    ans = ""
                    ans += "Вот ваша статистика калорий и БЖУ за сегодня:\n"
                    summ = float(user_data[0])
                    ans += "Ккал: " + str(user_data[1])
                    ans += "\nБелки: " + str(int(
                        float(user_data[2]) / summ * 100)) + " %"
                    ans += "\nЖиры: " + str(int(
                        float(user_data[3]) / summ * 100)) + " %"
                    ans += "\nУглеводы: " + str(int(
                        float(user_data[4]) / summ * 100)) + " %"
                    await bot.send_message(text=ans, chat_id=user_date.user_id)
                    data = await state_with.get_data()
                    data['calc_data'] = "ничего пока нет"
                    await orm_update_id(session, user_date.user_id, data)
                else:
                    await bot.send_message(text="Похоже сегодня вы ничего не ели. Надо подкрепиться!", chat_id=user_date.user_id)
            else:
                state_with: FSMContext = FSMContext(
                    storage=dp.storage,
                    key=StorageKey(
                        chat_id=user_date.user_id,
                        user_id=user_date.user_id,
                        bot_id=bot.id))
                await state_with.clear()


asyncio.get_event_loop().run_forever()