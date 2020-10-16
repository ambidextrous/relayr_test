import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler, Application
import aiosqlite

from config import PORT_ID, CACHE_MAX_LENGTH
from data_classes.data_classes import Supplier, Category, Product
from handlers.handlers import ProductSearchHandler, ProductPutHandler
from cache.cachedict import CacheDict


def make_app():
    app = Application(
        [
            (r"/product/search", ProductSearchHandler),
            (r"/product/put", ProductPutHandler),
        ]
    )
    app.cache_dict = CacheDict(cache_len=CACHE_MAX_LENGTH)
    return app


if __name__ == "__main__":
    app = make_app()
    app.listen(PORT_ID)
    tornado.ioloop.IOLoop.current().start()
