from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from core.config import settings



db = settings.DATABASE_URL

engine = create_async_engine(
    db,
    echo=True,
    poolclass = NullPool,
    # pool_size=20,
    # max_overflow=10,
    # pool_pre_ping=True,
    # pool_recycle=1800

    )

SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with SessionLocal() as session:
        yield session


async def get_current_user():
    pass

class Base(DeclarativeBase):
    pass
