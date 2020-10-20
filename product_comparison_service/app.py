import os
import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler, Application, StaticFileHandler
import aiosqlite

from product_comparison_service.config import (
    PORT_ID,
    CACHE_MAX_LENGTH,
    DATABASE,
    LOGGING_FILE,
)
from product_comparison_service.data_classes.data_classes import (
    Supplier,
    Category,
    Product,
)
from product_comparison_service.handlers.handlers import ProductHandler, DocsHandler
from product_comparison_service.cache.cachedict import CacheDict
from product_comparison_service.database.database import setup_database


def make_app():
    """
    Create tornado app and database populated with test data.
    """
    app = Application(
        [(r"/v0.1/product", ProductHandler), (r"/v0.1/docs", DocsHandler)]
    )
    app.cache = CacheDict(cache_len=CACHE_MAX_LENGTH)

    # Create and repopulate a fresh copy of the database for testing on app start-up
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    else:
        pass

    # Create database
    setup_database(DATABASE)

    # Use CLI tool to auto-populate database is with test data.
    os.system(
        "python product_comparison_service/cli.py add_products product_comparison_service/batch_processing_data/products.jsonl"
    )
    os.system(
        "python product_comparison_service/cli.py add_suppliers product_comparison_service/batch_processing_data/suppliers.jsonl"
    )
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
