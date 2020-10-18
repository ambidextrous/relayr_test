import os
import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler, Application, StaticFileHandler
import aiosqlite

from product_comparison_service.config import PORT_ID, CACHE_MAX_LENGTH, DATABASE, LOGGING_FILE
from product_comparison_service.data_classes.data_classes import Supplier, Category, Product
from product_comparison_service.handlers.handlers import ProductHandler, DocsHandler
from product_comparison_service.cache.cachedict import CacheDict
from product_comparison_service.database.database import setup_database


def make_app():
    app = Application(
        [
            (r"/v0.1/product", ProductHandler),
            (r"/v0.1/docs", DocsHandler),
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

    setup_database(DATABASE)

    os.system("python product_comparison_service/cli.py add_products product_comparison_service/batch_processing_data/products.jsonl")
    os.system("python product_comparison_service/cli.py add_suppliers product_comparison_service/batch_processing_data/suppliers.jsonl")
    os.system(
        "python product_comparison_service/cli.py add_supplier_products product_comparison_service/batch_processing_data/supplier_products.jsonl"
    )

    return app


if __name__ == "__main__":
    import logging

    logging.basicConfig(filename=LOGGING_FILE, level=logging.INFO)
    app = make_app()
    app.listen(PORT_ID)
    tornado.ioloop.IOLoop.current().start()
