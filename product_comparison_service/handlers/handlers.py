import json

from tornado.web import RequestHandler
import aiosqlite

from database.database import search_by_product_or_category
from config import DATABASE


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class ProductReadHandler(RequestHandler):
    async def get(self):
        product = self.get_argument("product", default=None)
        category = self.get_argument("category", default=None)
        conn = await aiosqlite.connect(DATABASE)
        conn.row_factory = dict_factory
        cursor = await conn.cursor()
        results = await search_by_product_or_category(
            conn=conn, cursor=cursor, product=product, category=category
        )
        self.write({"search_results": results})


class ProductWriteHandler(RequestHandler):
    async def put(self):
        product = self.get_arguments("product")
        category = self.get_arguments("category")
        self.write("Hello, put!")

    async def delete(self):
        product = self.get_arguments("product")
        category = self.get_arguments("category")
        self.write("Hello, delete!")
