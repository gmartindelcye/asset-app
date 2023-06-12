from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

# Create the SQLAlchemy engine
# engine = create_engine(settings.database_url)

# Create the async engine and session
async_engine = create_async_engine(settings.database_url, future=True)
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)

# Create a base class for declarative models
Base = declarative_base()


async def get_async_session() -> AsyncSession:
    """
    Return an async session from the async sessionmaker.
    """
    async with async_session() as session:
        yield session


a_session = get_async_session()
