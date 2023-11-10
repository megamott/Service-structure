from aiohttp.test_utils import TestClient
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from configuration.database.db_helper import DatabaseHelper


async def test_create_user_success(client: TestClient, db: DatabaseHelper) -> None:
    data = {"name": "NAME"}
    resp = await client.post("/api/v1/users/", json=data)
    assert resp.status == 201

    response_data = await resp.json()
    assert response_data == {**data, "id": 1}

    session: AsyncSession
    async with db.session() as session:
        result: Result = await session.execute(select(User).order_by(User.id))
        users = result.scalars().all()

    assert len(users) == 1


async def test_create_user_fail(client: TestClient, db: DatabaseHelper) -> None:
    data = {"name": 15}
    resp = await client.post("/api/v1/users/", json=data)
    assert resp.status == 400

    response_data = await resp.text()
    assert response_data == "User data is not correct"

    session: AsyncSession
    async with db.session() as session:
        result: Result = await session.execute(select(User).order_by(User.id))
        users = result.scalars().all()

    assert len(users) == 0


async def test_get_users_success(client: TestClient, db: DatabaseHelper) -> None:
    async with db.session() as session:
        user = User(name="NAME")
        session.add(user)
        await session.commit()
        await session.refresh(user)

    resp = await client.get("/api/v1/users/")
    assert resp.status == 200

    response_data = await resp.json()
    assert response_data == [{"name": user.name, "id": user.id}]

    session: AsyncSession
    async with db.session() as session:
        result: Result = await session.execute(select(User).order_by(User.id))
        users = result.scalars().all()

    assert len(users) == 1


async def test_get_user_success(client: TestClient, db: DatabaseHelper) -> None:
    session: AsyncSession
    async with db.session() as session:
        user = User(name="NAME")
        session.add(user)
        await session.commit()
        await session.refresh(user)

    resp = await client.get(f"/api/v1/users/{user.id}/")
    assert resp.status == 200

    response_data = await resp.json()
    assert response_data == {"name": user.name, "id": user.id}


async def test_get_user_fail(client: TestClient, db: DatabaseHelper) -> None:
    session: AsyncSession
    async with db.session() as session:
        user = User(name="NAME")
        session.add(user)
        await session.commit()
        await session.refresh(user)

    resp = await client.get(f"/api/v1/users/hello/")
    assert resp.status == 400

    response_data = await resp.text()
    assert response_data == "User id is not correct"

    not_existed_user_id = 1488
    resp = await client.get(f"/api/v1/users/{not_existed_user_id}/")
    assert resp.status == 404

    response_data = await resp.text()
    assert response_data == f"User {not_existed_user_id} not found"


async def test_update_user_success(client: TestClient, db: DatabaseHelper) -> None:
    session: AsyncSession
    async with db.session() as session:
        user = User(name="NAME")
        session.add(user)
        await session.commit()
        await session.refresh(user)

    new_name = "name"
    resp = await client.patch(f"/api/v1/users/{user.id}/", json={"name": new_name})
    assert resp.status == 200

    response_data = await resp.json()
    assert response_data == {"name": new_name, "id": user.id}

    session: AsyncSession
    async with db.session() as session:
        result: Result = await session.execute(select(User).order_by(User.id))
        users = result.scalars().all()
        assert len(users) == 1

        user = await session.get(User, int(user.id))
        assert user.name == new_name


async def test_update_user_fail(client: TestClient, db: DatabaseHelper) -> None:
    session: AsyncSession
    async with db.session() as session:
        user = User(name="NAME")
        session.add(user)
        await session.commit()
        await session.refresh(user)

    resp = await client.patch(f"/api/v1/users/{user.id}/", json={"name": 100})
    assert resp.status == 400

    response_data = await resp.text()
    assert response_data == "User data is not correct"

    resp = await client.patch("/api/v1/users/hello/", json={"name": "new_name"})
    assert resp.status == 400

    response_data = await resp.text()
    assert response_data == "User data is not correct"

    not_existed_user_id = 1488
    resp = await client.patch(f"/api/v1/users/{not_existed_user_id}/", json={"name": "new_name"})
    assert resp.status == 404

    response_data = await resp.text()
    assert response_data == f"User {not_existed_user_id} not found"


async def test_delete_user_success(client: TestClient, db: DatabaseHelper) -> None:
    session: AsyncSession
    async with db.session() as session:
        user = User(name="NAME")
        session.add(user)
        await session.commit()
        await session.refresh(user)

    resp = await client.delete(f"/api/v1/users/{user.id}/")
    assert resp.status == 200

    response_data = await resp.text()
    assert response_data == "User deleted successfully"

    session: AsyncSession
    async with db.session() as session:
        result: Result = await session.execute(select(User).order_by(User.id))
        users = result.scalars().all()
        assert len(users) == 0


async def test_delete_user_fail(client: TestClient, db: DatabaseHelper) -> None:
    session: AsyncSession
    async with db.session() as session:
        user = User(name="NAME")
        session.add(user)
        await session.commit()
        await session.refresh(user)

    resp = await client.delete(f"/api/v1/users/hello/")
    assert resp.status == 400

    response_data = await resp.text()
    assert response_data == "User id is not correct"

    not_existed_user_id = 1488
    resp = await client.delete(f"/api/v1/users/{not_existed_user_id}/")
    assert resp.status == 404

    response_data = await resp.text()
    assert response_data == f"User {not_existed_user_id} not found"

    session: AsyncSession
    async with db.session() as session:
        result: Result = await session.execute(select(User).order_by(User.id))
        users = result.scalars().all()
        assert len(users) == 1
