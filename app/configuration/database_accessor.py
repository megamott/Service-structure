from aiohttp import web

from app.configuration.config import Settings


class DatabaseAccessor:
    def __init__(self) -> None:
        from app.models.common import User

        self.user = User
        self.db = None

    def setup(self, app: web.Application) -> None:
        app.on_startup.append(self._on_connect)
        app.on_cleanup.append(self._on_disconnect)

    async def _on_connect(self, app: web.Application):
        from app.models import db

        self.config: Settings = app["config"]
        await db.set_bind(self.config.database_url)
        self.db = db

    async def _on_disconnect(self, _) -> None:
        if self.db is not None:
            await self.db.pop_bind().close()