"""Application dependencies."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency."""
    async with get_async_session() as session:
        yield session
