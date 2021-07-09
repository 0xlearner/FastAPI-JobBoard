from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import settings
from typing import Generator

SQLALCHMEY_DATABASE_URL = settings.DATABASE_URL
engine = create_async_engine(SQLALCHMEY_DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, autocommit=False, autoflush=False, class_=AsyncSession)

async def get_db() -> Generator:
    try:
        db = await async_session()
        yield db
    finally:
        db.close()