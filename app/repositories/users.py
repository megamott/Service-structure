from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.configuration.models.db_helper import DatabaseHelper
from app.models.users import User


class UserRepositoryInterface(ABC):

    @abstractmethod
    async def list(self): ...

    @abstractmethod
    async def retrieve(self, user_id: str): ...

    @abstractmethod
    async def create(self, user_data: dict): ...

    @abstractmethod
    async def update(self, user_id: str, user_data: dict): ...

    @abstractmethod
    async def delete(self, user_id: str) -> bool: ...


class UserRepository(UserRepositoryInterface):
    def __init__(self) -> None:
        self.db = DatabaseHelper()

    async def list(self) -> list[User]:
        session: AsyncSession
        async with self.db.session() as session:
            result: Result = await session.execute(select(User).order_by(User.id))
            users = result.scalars().all()

        return list(users)

    async def retrieve(self, user_id: str) -> Optional[User]:
        session: AsyncSession
        async with self.db.session() as session:
            user = await session.get(User, int(user_id))
        return user

    async def create(self, user_data: dict) -> User:
        session: AsyncSession
        async with self.db.session() as session:
            user = User(**user_data)
            session.add(user)
            await session.commit()
            await session.refresh(user)

        return user

    async def update(self, user_id: str, user_data: dict) -> Optional[User]:
        session: AsyncSession
        async with self.db.session() as session:
            user = await session.get(User, int(user_id))

            if not user:
                return None

            for name, value in user_data.items():
                setattr(user, name, value)

            await session.commit()
            await session.refresh(user)

        return user

    async def delete(self, user_id: str) -> bool:
        session: AsyncSession
        async with self.db.session() as session:
            user = await session.get(User, int(user_id))

            if not user:
                return False

            await session.delete(user)
            await session.commit()

        return True
