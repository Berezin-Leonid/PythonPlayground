from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
import asyncio
from config import PRICE, DATABASE_URL 

# Создание движка SQLAlchemy
#engine = create_async_engine("postgresql+asyncpg://localhost/Voenka")
engine = create_async_engine(DATABASE_URL) 
async_session = async_sessionmaker(engine, class_=AsyncSession)

# Создание базового класса для моделей
class Base(AsyncAttrs, DeclarativeBase):
    pass



# Таблица Platoon
class Platoon(Base):
    __tablename__ = 'platoon'
    
    index = Column(Integer, primary_key=True, autoincrement=True)  # IDENTITY аналог в PostgreSQL
    name = Column(String, nullable=False, unique=True)

    # Связь с Soldier
    soldiers = relationship('Soldier', back_populates='platoon')

# Таблица Soldier
class Soldier(Base):
    __tablename__ = 'soldier'
    
    index = Column(Integer, primary_key=True, autoincrement=True)  # IDENTITY аналог в PostgreSQL
    tg_id = Column(BigInteger, nullable=False, unique=True)
    tg_name = Column(String, nullable=True, unique=True)
    platoon_id = Column(Integer, ForeignKey('platoon.index'), nullable=False)

    # Связь с Platoon
    platoon = relationship('Platoon', back_populates='soldiers')
    
    # Связь с Order
    orders = relationship('Orders', back_populates='soldier')

# Таблица Order
class Orders(Base):
    __tablename__ = 'orders'
    
    index = Column(Integer, primary_key=True, autoincrement=True) 
    soldier_id = Column(BigInteger, ForeignKey('soldier.index'), nullable=False)
    photo_path = Column(String, nullable=True)
    photo_count = Column(Integer, nullable=False, default=3)
    make_name = Column(Integer, nullable=False, default=0)
    price = Column(Integer, nullable=False, default=PRICE)

    # Связь с Soldier
    soldier = relationship('Soldier', back_populates='orders')
    
    # Связь с Blanked
    blanked = relationship('Blanked', back_populates='orders')

# Таблица Blanked
class Blanked(Base):
    __tablename__ = 'blanked'
    
    index = Column(Integer, primary_key=True, autoincrement=True)  # IDENTITY аналог в PostgreSQL
    orders_id = Column(Integer, ForeignKey('orders.index'), nullable=False)

    # Связь с Order
    orders = relationship('Orders', back_populates='blanked')


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(async_main())
