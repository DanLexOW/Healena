import os

import aiocron
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm import storage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import logging
from main import storage, FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.base import StorageKey


TOKEN = '7142739750:AAGyfmowTD29-ZcllG_13JGdMDoDJ3HCbIE'
token = os.getenv("TOKEN")
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(storage=storage)


@aiocron.crontab('* * * * *')
async def hi():
    state_with: FSMContext = FSMContext(
        storage=dp.storage,
        key=StorageKey(
            chat_id=1717310606,
            user_id=1717310606,
            bot_id=bot.id))
    user_data = await state_with.get_data()
    print(user_data)
    if 'summ' in user_data:
        ans = ""
        ans += "Вот ваша статистика калорий и БЖУ за сегодня:\n"
        summ = user_data['summ']
        ans += "Количество ккал - " + str(user_data['cal'])
        ans += "\nПроцентное соотношение белка ко всей съеденной за сегодня пище составляет " + str(int(
            float(user_data['protein']) / summ * 100)) + " процентов"
        ans += "\nПроцентное соотношение жиров ко всей съеденной за сегодня пище составляет " + str(int(
            float(user_data['fat']) / summ * 100)) + " процентов"
        ans += "\nПроцентное соотношение углеводов ко всей съеденной за сегодня пище составляет " + str(int(
            float(user_data['carbohydrate']) / summ * 100)) + " процентов"
        await bot.send_message(text=ans, chat_id="1717310606")
        await state_with.clear()
    else:
        await bot.send_message(text="Похоже сегодня вы ничего не ели. Возвращайтесь, когда подкрепитесь", chat_id="1717310606")
    '''print('hello!')
    await bot.send_message(text="Hello there!", chat_id="1717310606")'''

asyncio.get_event_loop().run_forever()