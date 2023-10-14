# Singleton = klass ise vastutab mulle enda instance andmise eest,
# Seal sees on funktsioon mis annab mulle tema instance kui seda pole, siis ta loob
# ja järgmisel seadmisel ta annab mulle selle mis ta enne lõi

# Variant 2
# Iga kord, kui ma seda klassi tahan kasutada, teen ta nullist

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
