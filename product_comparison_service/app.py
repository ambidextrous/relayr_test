import os
import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler, Application
import aiosqlite

from config import PORT_ID, CACHE_MAX_LENGTH, DATABASE
from data_classes.data_classes import Supplier, Category, Product
from handlers.handlers import ProductReadHandler, ProductWriteHandler
from cache.cachedict import CacheDict
from database.database import setup_database

def make_app():
    app = Application(
        [
            (r"/product/search", ProductReadHandler),
            (r"/product/update", ProductWriteHandler),
        ]
    )
    app.cache = CacheDict(cache_len=CACHE_MAX_LENGTH)

    # TODO: remove
    # While in development, create fresh DB instance for each run
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print(f"{DATABASE} deleted")
    else:
        print(f"{DATABASE} does not exist")

    app.db = setup_database(DATABASE)
    return app


if __name__ == "__main__":
    app = make_app()
    app.listen(PORT_ID)
    tornado.ioloop.IOLoop.current().start()
