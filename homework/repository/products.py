class ProductsRepository:
    def __init__(self, connection):
        self.connection = connection

    def find_all_products(self):
        return self.connection.execute('select id, name, price from products order by id').fetchall()

    def find_product_by_id(self, product_id):
        return self.connection.execute('select id, name, price from products where id = ?', (product_id,)).fetchone()
