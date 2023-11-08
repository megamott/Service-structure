from aiohttp import web

from app.configuration.server import Server


async def create_app() -> web.Application:
    app = web.Application()

    return Server(app).get_app()
