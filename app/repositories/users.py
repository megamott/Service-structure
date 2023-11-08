from typing import Optional

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.configuration.models.db_helper import db_helper
from app.models.users import User


class UserRepository:
    def __init__(self) -> None:
        self.db_helper = db_helper
        self.session: AsyncSession = db_helper.get_session()

    async def list(self) -> list[User]:
        statement = select(User).order_by(User.id)

        session: AsyncSession
        async with self.session() as session:
            result: Result = await session.execute(statement)
            users = result.scalars().all()

        return list(users)
    
    async def retrieve(self, user_id: int) -> Optional[User]:
        session: AsyncSession
        async with self.session() as session:
            return await session.get(User, user_id)
    
    async def create(self, user_data: dict) -> User:
        user = User(**user_data)

        session: AsyncSession
        async with self.session() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)

        return user
