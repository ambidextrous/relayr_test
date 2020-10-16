from tornado.web import RequestHandler

from product_comparison_service.database.database import search_by_product_or_category


class ProductSearchHandler(RequestHandler):
    async def get(self):
        product = self.get_arguments("product")
        category = self.get_arguments("category")
        results = await search_by_product_or_category(
            product=product, category=category
        )
        return results


class ProductPutHandler(RequestHandler):
    def put(self):
        self.write("Hello, put!")
