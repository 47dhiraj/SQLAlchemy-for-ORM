from typing import AsyncGenerator, Annotated
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase




DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost:5432/async_sqla_db"




async_engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,  
    pool_recycle=1200,  
    pool_timeout=20,     
    pool_pre_ping=True,
    echo=True
    # echo=False
)  


AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,    
    class_=AsyncSession,    
    # autoflush=False,
    expire_on_commit=False
)




class Base(DeclarativeBase):
    pass




DatabaseSession = Annotated[AsyncSession, "Active asynchronous database transaction context"]


async def get_db() -> AsyncGenerator[DatabaseSession, None]:

    async with AsyncSessionLocal() as session:
        yield session
