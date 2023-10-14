from uuid import uuid4


class OrdersRepository:
    def __init__(self, connection):
        self.connection = connection

    def order_exists(self, order_id):  # TODO: maybe this is not needed, find_order_by_id() can do the same
        row = self.connection.execute('select 1 from orders where id = ?', (order_id,)).fetchone()
        return bool(row)

    def create_new_order(self):
        order_id = str(uuid4())
        self.connection.execute('insert into orders (id) values (?)', (order_id,))
        return order_id

    def find_order_by_id(self, order_id):
        # TODO: Calculate total
        query = 'select id, status, discount, paid, returns, 0.0 as total from orders where id = ?'
        return self.connection.execute(query, (order_id,)).fetchone()

    def find_order_products_by_order_id(self, order_id):
        query = '''
        select op.id,
               p.name,
               p.price,
               op.product_id,
               op.quantity,
               r.id as r_id,
               rp.name as r_name,
               rp.price as r_price,
               rp.id as r_product_id,
               r.quantity as r_quantity
        from order_products as op
        join products as p on op.product_id = p.id
        left join replacements as r on op.id = r.original_id
        left join products as rp on r.product_id = rp.id
        where op.order_id = ?
        '''
        return self.connection.execute(query, (order_id,)).fetchall()

    def update_order_status_by_id(self, order_id, new_status):
        cursor = self.connection.execute('update orders set status = ? where id = ?', (new_status, order_id))
        return cursor.rowcount

    def add_products_to_order(self, order_id, product_ids):
        insert_query = 'insert or ignore into order_products (id, order_id, product_id, quantity) values (?, ?, ?, 1)'
        update_query = 'update order_products set quantity = quantity + 1 where order_id = ? and product_id = ?'

        rows_affected = 0
        for product_id in product_ids:
            order_product_id = str(uuid4())
            cursor = self.connection.execute(insert_query, (order_product_id, order_id, product_id))
            if cursor.rowcount == 0:
                cursor = self.connection.execute(update_query, (order_id, product_id))
            rows_affected += cursor.rowcount
        return rows_affected

    def update_quantity(self, order_id, product_uuid, quantity):
        cursor = self.connection.execute('update order_products set quantity = ? where order_id = ? and id = ?',
                                         (quantity, order_id, product_uuid))
        return cursor.rowcount

    def insert_replacement_product(self, old_product_uuid, replacement_id, quantity):
        replacement_uuid = str(uuid4())
        query = 'insert into replacements (id, original_id, product_id, quantity) values (?, ?, ?, ?)'
        cursor = self.connection.execute(query, (replacement_uuid, old_product_uuid, replacement_id, quantity))
        return cursor.rowcount
