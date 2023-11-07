from aiohttp import web

from app.repositories.common import UserRepository
from app.models.common import User

router = web.RouteTableDef()


@router.get("/ping/")
async def ping(request: web.Request):
    return web.Response(text="OK")


@router.get("/users/")
async def users(request: web.Request):
    users: list[User] = await UserRepository().all()
    return web.Response(text=', '.join([user.name for user in users]))