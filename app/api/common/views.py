from aiohttp import web

router = web.RouteTableDef()


@router.get("/ping/")
async def ping(request: web.Request):
    return web.Response(text="OK")