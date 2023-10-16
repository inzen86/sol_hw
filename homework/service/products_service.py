from homework.repository.model.product import Product
from homework.repository.products import ProductsRepository


class ProductsService:
    def __init__(self, connection):
        self.connection = connection
        self.repository = ProductsRepository(self.connection)

    def get(self):
        rows = self.repository.find_all_products()

        products = []
        for row in rows:
            products.append(Product.from_row(row))
        return products
