import aiofiles

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config_data.config import _CONFIG
from database.models import Base
from database.models import User, Word


engine = create_async_engine(_CONFIG.db.DSN()) # , echo=True)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def insert_db():
    async with session_maker() as session:
        new_data = User(user_id=1, name='Default')
        session.add(new_data)
        async with aiofiles.open('top_100.txt', 'r', encoding='utf-8') as file:
            async for line in file:
                if line.strip():
                    _, words = line.split('.')
                    en, ru = words.split('–')
                    new_data = Word(word_eng=en.strip().capitalize(),
                                    word_rus=ru.strip().capitalize())
                    session.add(new_data)
        await session.commit()

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
