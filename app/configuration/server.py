from aiohttp import web

from app.configuration.routes import routers


class Server:
    _app: web.Application

    def __init__(self, app: web.Application) -> None:
        self._app = app
        self._register_routes(app)

    def get_app(self) -> web.Application:
        return self._app

    @staticmethod
    def _register_routes(app) -> None:
        routers.register_routes(app)
