from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from data_base.models import Training, Product


async def orm_get_products(session: AsyncSession):
    query = select(Product)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_product(session: AsyncSession, product_name: str):
    query = select(Product).where(Product.name == product_name)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_training(session: AsyncSession, training_id: int):
    query = select(Training).where(Training.id == training_id)
    result = await session.execute(query)
    return result.scalar()






