import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from data_base.models import Base  #импорт из models.py

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


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

