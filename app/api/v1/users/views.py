from aiohttp import web

from app.repositories.common import UserRepository
from app.models.common import User

router = web.RouteTableDef()


@router.get("/api/v1/users/")
async def users(request: web.Request):
    users: list[User] = await UserRepository().list()
    return web.Response(text=', '.join([user.name for user in users]))