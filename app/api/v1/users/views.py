from aiohttp import web

from app.repositories.users import UserRepository
from app.models.users import User as UserModel
from app.api.v1.users.schemas import UserCreate

router = web.RouteTableDef()


@router.get("/api/v1/users/")
async def get_users(request: web.Request) -> web.Response:
    users: list[UserModel] = await UserRepository().list()
    return web.json_response([user.as_dict() for user in users])


@router.post("/api/v1/users/")
async def create_user(request: web.Request) -> web.Response:
    user_data = await request.json()
    user: UserModel = await UserRepository().create(UserCreate(**user_data).model_dump())
    return web.json_response(user.as_dict())