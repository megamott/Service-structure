from aiohttp import web


class Events:
    def register_events(self, app: web.Application) -> None:
        ...


events = Events()
