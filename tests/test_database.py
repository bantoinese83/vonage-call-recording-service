import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import init_db, async_session

@pytest.mark.asyncio
async def test_init_db():
    async with async_session() as session:
        assert isinstance(session, AsyncSession)
        await init_db()
        # Add any additional assertions or checks if needed
