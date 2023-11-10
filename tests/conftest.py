import json
import asyncio
from typing import Any

import pytest
from unittest import mock
from sqlalchemy.ext.asyncio import AsyncSession

from app.configuration.config import Settings
from app import create_app
from app.configuration.database.base import Base
from app.configuration.database.db_helper import DatabaseHelper


settings = Settings(**{
    "database_url": "postgresql+asyncpg://postgres:postgres@localhost:6432/postgres",
    "database_echo": True,
})


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def app_settings_mock():
    with mock.patch("app.configuration.config._read_settings", return_value=settings) as app_settings_mock:
        yield app_settings_mock


@pytest.fixture
async def client(aiohttp_client: Any, app_settings_mock: mock.MagicMock):
    app = await create_app()
    return await aiohttp_client(app)


@pytest.fixture(scope="session")
async def db(app_settings_mock: mock.MagicMock):
    db_helper = DatabaseHelper()
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return db_helper


@pytest.fixture(scope="function", autouse=True)
async def truncate_tables():
    """ Чистит таблицы перед каждым тестом """
    db_helper = DatabaseHelper()
    session: AsyncSession
    async with db_helper.session() as session:
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
            await session.commit()
    yield
