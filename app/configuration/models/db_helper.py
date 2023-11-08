from asyncio import current_task

from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    async_sessionmaker, create_async_engine)

from app.configuration.config import get_settings


class DatabaseHelper:
    def __init__(self, database_url: str, echo: bool) -> None:
        self.engine = create_async_engine(
            url=database_url,
            echo=echo,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    def get_session(self) -> AsyncSession:
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session


settings = get_settings()
db_helper = DatabaseHelper(
    database_url=settings.database_url,
    echo=settings.database_echo,
)
