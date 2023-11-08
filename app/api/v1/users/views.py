from aiohttp import web
from pydantic import ValidationError

from app.api.v1.users.schemas import (
    UserCreateValidator,
    UserIdValidator,
    UserValidator,
)
from app.repositories.users import UserRepository

router = web.RouteTableDef()


@router.get("/api/v1/users/")
async def get_users(request: web.Request) -> web.Response:
    users = await UserRepository().list()

    return web.json_response(
        [UserValidator(**user.as_dict()).model_dump() for user in users]
    )


@router.get("/api/v1/users/{user_id}/")
async def get_user(request: web.Request) -> web.Response:
    user_id = request.match_info.get("user_id")
    try:
        UserIdValidator.model_validate({"id": user_id})
    except ValidationError:
        raise web.HTTPBadRequest(text="User id is not correct")

    user = await UserRepository().retrieve(user_id)
    if user is not None:
        return web.json_response(user.as_dict())

    raise web.HTTPNotFound(text=f"User {user_id} not found")


@router.post("/api/v1/users/")
async def create_user(request: web.Request) -> web.Response:
    user_data = await request.json()

    try:
        UserCreateValidator.model_validate(user_data)
    except ValidationError:
        raise web.HTTPBadRequest(text="User data is not correct")

    user = await UserRepository().create(user_data)

    return web.json_response(user.as_dict())


@router.patch("/api/v1/users/{user_id}/")
async def update_user(request: web.Request) -> web.Response:
    user_id = request.match_info.get("user_id")
    user_data = await request.json()

    try:
        UserCreateValidator.model_validate(user_data)
        UserIdValidator.model_validate(user_id)
    except ValidationError:
        raise web.HTTPBadRequest(text="User data is not correct")

    user = await UserRepository().update(user_id, user_data)

    if user is not None:
        return web.json_response(user.as_dict())
    raise web.HTTPNotFound(text=f"User {user_id} not found")


@router.delete("/api/v1/users/{user_id}/")
async def delete_user(request: web.Request) -> web.Response:
    user_id = request.match_info.get("user_id")

    try:
        UserIdValidator.model_validate({"id": user_id})
    except ValidationError:
        raise web.HTTPBadRequest(text="User id is not correct")

    deleted = await UserRepository().delete(user_id)

    if deleted:
        return web.Response(text="User deleted successfully")
    raise web.HTTPNotFound(text=f"User {user_id} not found")
