from tornado.web import RequestHandler

from database.database import search_by_product_or_category


class ProductReadHandler(RequestHandler):
    async def get(self):
        product = self.get_arguments("product")
        category = self.get_arguments("category")
        results = await search_by_product_or_category(
            product=product, category=category
        )
        return results


class ProductWriteHandler(RequestHandler):
    async def put(self):
        product = self.get_arguments("product")
        category = self.get_arguments("category")
        self.write("Hello, put!")

    async def delete(self):
        product = self.get_arguments("product")
        category = self.get_arguments("category")
        self.write("Hello, delete!")
