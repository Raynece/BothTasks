from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine('postgresql+asyncpg://postgres:1234@localhost:5432/TestTask', echo = False)
async_session_maker = async_sessionmaker(bind=engine,expire_on_commit=False,class_=AsyncSession)
# DB_HOST = 'localhost'
# DB_PORT = 5432
# DB_USER = '1234'
# DB_PASS = '1234'
# DB_NAME = '1234'
#
# DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
class Base(DeclarativeBase):
    pass

