from aiohttp import web

from app.configuration.database_accessor import DatabaseAccessor


class Events:
    def register_events(self, app: web.Application) -> None:
        self._add_database_accessor(app)

    def _add_database_accessor(self, app: web.Application) -> None:
        app["db"] = DatabaseAccessor()
        app["db"].setup(app)


events = Events()