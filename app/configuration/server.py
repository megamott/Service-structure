from aiohttp import web

from app.configuration.routes import routers
from app.configuration.events import events
from app.configuration.config import setup_config


class Server:
    _app: web.Application

    def __init__(self, app: web.Application) -> None:
        self._app = app
        self._setup_config(app)
        self._register_routes(app)
        self._register_events(app)

    def get_app(self) -> web.Application:
        return self._app

    @staticmethod
    def _register_routes(app: web.Application) -> None:
        routers.register_routes(app)

    @staticmethod
    def _setup_config(app: web.Application) -> None:
        setup_config(app)

    @staticmethod
    def _register_events(app: web.Application) -> None:
        events.register_events(app)
