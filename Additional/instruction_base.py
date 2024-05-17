'''
#БФ: я посмотрела не весь 7й ролик, а только час. Не успела к сожалению. Всё до инлайн-кнопок. Постараюсь досмотреть по возможности

#установить библиотеки в терминале-----------------------------------------------
pip install sqlalchemy
pip install aiosqlite
(pip install asyncpg) - #не понадобится скорее всего

#папки и файлы, которые нужны----------------------------------------------------
#текстовый файл .env для записи url
#dp.py - создание сессий
#папка database
    #файл для записи движка - engine.py
    #файл для описания таблиц - models.py
    #файл для действий с базой данных - orm_query
#файл в папке handlers - admin_private.py для ответов бота

#models.py-----------------------------------------------------------------------
#описание таблиц -  (1) создание самой таблицы через питон
#                    (2) создание названия таблицы и названий столбцов
from sqlalchemy import String, Text, Float, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now()) #должно происходить автоматически, либо вручную ручками записывать в базу
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class Product(Base): (1)
    __tablename__ = 'product'   #примерное название таблицы; названия + характеристики столбцов ниже, они примерные

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False) #макс кол-во симв = 150, не может быть пустым
    description: Mapped[str] = mapped_column(Text) #поле с большим текстом
    price: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    image: Mapped[str] = mapped_column(String(150)) #id of image

#engine.py---------------------------------------------------------------------------
#движок

import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from database.models import Base  #импорт из models.py

#from .env file: #об url, не убирать комменты
# DB_LITE=sqlite+aiosqlite:///my_base.db
# DB_URL=postgresql+asyncpg://login:password@localhost:5432/db_name
# engine = create_async_engine(os.getenv('DB_LITE'), echo=True)

engine = create_async_engine(os.getenv('DB_URL'), echo=True) #название url тут нужно, это Движок

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False) #для создания сессий

#чтобы создать таблицу, код ниже
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

#чтобы удалить все таблицы. Нам не нужно, возможно
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


#app.py (главная программа)------------------------------------------------------------
###в конце, до функции async def main()

async def on_startup(bot):

    run_param = False
    if run_param:
        await drop_db() #+импортируем

    await create_db()


async def on_shutdown(bot):
    print('бот лег')

### под async def main():

    dp.startup.register(on_startup) #чтобы работало во время старта/завершения бота
    dp.shutdown.register(on_shutdown)

#запуск таблицы, там же
    await create.db() #+импортируем
#!!! этот импорт должен быть после from dotenv... и load dotenv...

#.env, после токена-----------------------------------------------------------------
#(название можно с LITE, но у меня такое)
DB_URL=sqlite+aiosqlite:///my_base.db
#можно полный адрес написать для точности


#++++++++++++++++++++++++++++++++++++++++++++++!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#запустить проверить, всё ли работает. Должна создаться база данных my_base.db рядом с файлами
#ещё в выводе должно быть что-то такое

#2024-05-07 13:34:03,146 INFO sqlalchemy.engine.Engine BEGIN (implicit)
#2024-05-07 13:34:03,146 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("product")
#2024-05-07 13:34:03,146 INFO sqlalchemy.engine.Engine [raw sql] ()
#2024-05-07 13:34:03,147 INFO sqlalchemy.engine.Engine COMMIT


#если всё работает, НАДО СКАЧАТЬ ПРИЛОЖЕНИЕ НА КОМП: DB Browser (SQLite) (серый цилиндр), подходит только для типа sqlite
#открыть приложение
# open database сверху
#выбрать my_base.db

#см. фото 1, там таблица product создана с характеристиками столбцов
#переходим в browse data (Данные), см фото 2
# там должны быть именованные столбцы, без строчек. Можно тыкнуть и посмотреть их характеристики


###ДАЛЬШЕ - ЗАПОМНЯЕМ ВРУЧНУЮ ТАБЛИЦУ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++!!!!!!!!!!!!!!!!!!!!!!!!
#см фото 3 - список с плюсиком - создание строчки
#сама запись в строчку
#!!!!!!!!!!! сохранение ручных записей в строчки, см фото 4, "Записать изменения" (будет светиться)

#ЕСЛИ ХОЧЕТСЯ ЧЕРЕЗ ПРОГРАММУ----------------------------------------------------------
#то, что в видео, нам не подойдёт
#он делает сессии так, чтобы изменять/добавлять строчки можно было через админку в тг. Нам это не надо.
#поэтому нам лучше вручную
#однако вручную я хз, как фотки передавать, буквами. Видимо, либо мы без картинок, либо какой-то другой тип столбцов нужен
#я пыталась добавлять через питон, но у меня

    #description=data["description"],
#KeyError: 'description'

#и всё тут.
#так что файл orm_query.py нужен только частично. В нём можно создать функцию для вывода ассортимента (то есть таблицы). Это я дальше напишу

#дальше создать dp.py чисто чтобы сессии подключить--------------------------------------------------------------------
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker


class DataBaseSession(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool #передаём session_maker


    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data['session'] = session
            return await handler(event, data)

#создаём orm_query.py------------------------------------------------------------------------
#действия с базой данных

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Product


async def orm_add_product(session: AsyncSession, data: dict):  #не нужно, вручную
    obj = Product(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"],
    )
    session.add(obj)
    await session.commit()


async def orm_get_products(session: AsyncSession):   #будут выбраны все записи из этой таблицы
    query = select(Product)
    result = await session.execute(query) #выполнить запрос - передаём
    return result.scalar()
    return result.scalars().all()


async def orm_get_product(session: AsyncSession, product_id: int): #получать определённый продукт
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)


async def orm_update_product(session: AsyncSession, product_id: int, data): #обновление данных, вручную, не нужно
    query = update(Product).where(Product.id == product_id).values(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"],)
    await session.execute(query)
    await session.commit()


async def orm_delete_product(session: AsyncSession, product_id: int): #удаление существующей записи, вероятно не нужно
    query = delete(Product).where(Product.id == product_id)
    await session.execute(query)
    await session.commit()

#в admin_private.py - оч важный код---------------------------------------------------------------------------------

#создание кнопки-клавы (чисто пример)
ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Ассортимент",
    placeholder="Выберите действие",
    sizes=(2,),
)

#создание команды
@admin_router.message(Command("admin"))
async def admin_features(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


#исполнение одной из кнопок (Ассортимент). Выведет данные, которые попросишь из таблицы. В данном случае - а-ля картинку, имя и описание.
#Однако я не научилась отправлять в базу картинки. Так что пробовала просто с текстом. ОДНАКО я кое-что нашла, см дальше:)
#Вторую кнопку не смогла починить. Туда принимается на вход машина состояний. И в конце, после заполнения, инфа добавляется в таблицу. Мы вручную

@admin_router.message(F.text == "Ассортимент")
async def starring_at_product(message: types.Message, session: AsyncSession): с сессией:аннотация
    for product in await orm_get_products(session): #команду импортируем
        await message.answer(   # тут стояло answer_photo, тк надо было, чтобы фото отправлялось. Об этой функции подробнее ниже
            product.image,
            caption=f"<strong>{product.name}\   #выводит картинку, имя и описание
                    </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}",
        ),
        await message.answer(product.description)
    await message.answer("ОК, вот список товаров ⏫")

#что такое сессия
#сессия - это обращение к таблице
#Данные, которые на данный момент доступны/существуют. Во время сессии происходят изменения, если изменять таблицу. Сессия закончена, когда закончил работать с таблицей, закоммитил
#Во время сессии к базе может обратиться один человек и работать с ней до коммита.

#У этой команды разные возможности. Можно str передать - идентификатор от машины состояния:

#{'name': 'пицца', 'describtion': 'круглая такая', 'price': '100', 'image': 'AgACAgIAAxkBAAIB52Y1B9p5KmoMbOl09znf5nvHnYvjAAIk3zEbfDapSY7SoHadyDjCAQADAgADeAADNAQ'}

#однако после подключения базы почему-то не работает у меня.
#а можно отправить фотку через путь #InputFile, см 7й ролик 53:30, секунд 20




caption = описание изображения
'''
