from tornado.web import RequestHandler


class ProductSearchHandler(RequestHandler):
    def get(self):
        product_id = self.get_arguments("product")
        category_id = self.get_arguments("category")
        self.write(f"product={product_id}; category={category_id}")


class ProductPutHandler(RequestHandler):
    def put(self):
        self.write("Hello, put!")