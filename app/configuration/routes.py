from dataclasses import dataclass

from aiohttp import web

from app.api.common import views as common_views


@dataclass(frozen=True)
class Routers:
    routers: tuple

    def register_routes(self, app: web.Application) -> None:
        for router in self.routers:
            app.add_routes(router)


routers = Routers(
    routers=(
        common_views.router,
    )
)
