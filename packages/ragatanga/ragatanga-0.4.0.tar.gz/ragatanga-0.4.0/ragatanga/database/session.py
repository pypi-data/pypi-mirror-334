"""
SQLAlchemy session management.

This module provides functions for managing SQLAlchemy sessions.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import text

from ragatanga.config import DATABASE_URL, DB_ECHO
from ragatanga.database.tables import metadata

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=DB_ECHO,
    future=True,
    # Only use NullPool for SQLite - for PostgreSQL, let SQLAlchemy handle connection pooling
    poolclass=NullPool if DATABASE_URL.startswith("sqlite") else None,
)

# Create async session factory
async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def init_db() -> None:
    """
    Initialize the database by creating all tables.
    
    This function should be called when the application starts.
    """
    async with engine.begin() as conn:
        # For PostgreSQL, enable the uuid-ossp extension for UUID functions
        if 'postgresql' in DATABASE_URL:
            await conn.execute(
                text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
            )
        await conn.run_sync(metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get a SQLAlchemy async session.
    
    This function is intended to be used as a dependency in FastAPI.
    
    Yields:
        AsyncSession: A SQLAlchemy async session
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close() 