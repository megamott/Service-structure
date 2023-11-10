from asyncio import current_task
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.configuration.config import get_settings


class DatabaseHelper:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DatabaseHelper, cls).__new__(cls)
            cls.instance._initialized = False
        return cls.instance

    def __init__(self) -> None:
        if self._initialized:
            return
        settings = get_settings()

        self.engine = create_async_engine(
            url=settings.database_url,
            echo=settings.database_echo,
        )

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

        self._initialized = True

    @asynccontextmanager
    async def session(self) -> AsyncSession:
        scoped_factory = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        try:
            async with scoped_factory() as s:
                yield s
        finally:
            await scoped_factory.remove()
