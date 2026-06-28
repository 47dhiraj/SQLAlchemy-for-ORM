from contextlib import asynccontextmanager

from typing import AsyncGenerator, TypeAlias

from sqlalchemy import text

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from sqlalchemy.orm import DeclarativeBase






DatabaseSession: TypeAlias = AsyncSession



class Base(DeclarativeBase):
    pass




DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost:5432/sql_explicit_db"



engine = create_async_engine(DATABASE_URL, pool_size=10, max_overflow=10, echo=True)




AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False, 
    # autoflush=False
)






@asynccontextmanager
async def get_db() -> AsyncGenerator[DatabaseSession, None]:
    """
        Yields a database session. Automatically closes (.close()) the session on exit.
    """

    async with AsyncSessionLocal() as session:
        yield session




async def init_db() -> None:
    """
        Registers schemas and builds missing database tables natively inside PostgreSQL.
    """

    import models                   ## importing models for prevention of any prior crash

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)           ## this line requires our model to be loaded prior





async def close_db() -> None:
    """
        Safely terminates (.dispose()) the entire global connection socket pool on exit.
    """

    await engine.dispose()





async def ping_db() -> bool:
    """
        Isolated, direct diagnostic check to verify if the database server is online.
    """

    try:
        async with AsyncSessionLocal() as session:
            
            await session.execute(text("SELECT 1"))
            return True
        
    except Exception:
        return False
