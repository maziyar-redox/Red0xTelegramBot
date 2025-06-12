from aiohttp import web
from .stream_routes import routes

def web_server():
    web_app = web.Application(client_max_size=3000000)
    web_app.add_routes(routes)
    return web_app