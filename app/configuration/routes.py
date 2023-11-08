from dataclasses import dataclass

from aiohttp import web

from app.api.v1.common import views as v1_common_views
from app.api.v1.users import views as v1_users_views


@dataclass(frozen=True)
class Routers:
    routers: tuple

    def register_routes(self, app: web.Application) -> None:
        for router in self.routers:
            app.add_routes(router)


routers = Routers(
    routers=(
        v1_common_views.router,
        v1_users_views.router,
    )
)
