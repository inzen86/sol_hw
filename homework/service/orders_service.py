from homework.repository.model.order import Order, OrderProduct
from homework.repository.orders import OrdersRepository


class OrderService:
    def __init__(self, connection, products_service=None):
        self.connection = connection
        self.order_repository = OrdersRepository(self.connection)
        self.products_service = products_service

    def create_and_get(self):
        order_id = self.order_repository.create_new_order()
        self.connection.commit()
        return self.get(order_id)

    def get(self, order_id):
        order_row = self.order_repository.find_order_by_id(order_id)
        if not order_row:
            return
        order = Order.from_row(order_row)
        order_products = self.get_products(order_id)
        if not order_products:
            return order
        order.products = order_products
        return order

    def get_products(self, order_id):
        order_products_rows = self.order_repository.find_order_products_by_order_id(order_id)
        if order_products_rows is None:
            return
        order_products = [OrderProduct.from_row(r) for r in order_products_rows]
        return order_products

    def update_status(self, order_id, new_status):
        order_row = self.order_repository.find_order_by_id(order_id)
        if not order_row:
            return 'Not found', 404
        order = Order.from_row(order_row)
        if order.status != 'NEW' or new_status != 'PAID':
            return 'Invalid order status', 400
        if order.status == 'NEW' and new_status == 'PAID':
            rowcount = self.order_repository.update_order_status_by_id(order_id, new_status)
            if rowcount == 1:
                self.connection.commit()
                return 'OK', 200
        return None, None

    def add_products(self, order_id, request_product_ids):

        order = self.get(order_id)
        if not order:  # Check if order exists
            return

        if not isinstance(request_product_ids, list):
            return

        product_ids = self.validate_product_ids(request_product_ids)
        if not product_ids:
            return

        rows_affected = self.order_repository.add_products_to_order(order_id, product_ids)
        if rows_affected:
            self.connection.commit()
        else:
            self.connection.rollback()
        return rows_affected

    def validate_product_ids(self, product_ids) -> list:
        validated_ids = []
        existing_product_ids = self._product_ids()

        for product_id in product_ids:
            if product_id in validated_ids:  # Check for duplicates
                return []
            if product_id not in existing_product_ids:  # Check if product exists
                return []
            validated_ids.append(product_id)

        return validated_ids

    def _product_ids(self):
        products = self.products_service.get()
        return [product.id for product in products]

    def update_quantity(self, order_id, product_uuid, quantity):
        order = self.get(order_id)
        if not order:
            return 'Not found', 404
        if order.status == 'PAID':
            return 'Invalid parameters', 404
        rows_affected = self.order_repository.update_quantity(order_id, product_uuid, quantity)
        if rows_affected:
            self.connection.commit()
            return 'OK', 200

        self.connection.rollback()
        return None, None

    def replace_product(self, order_id, product_uuid, replacement_id, replacement_quantity):
        order = self.get(order_id)
        if not order:
            return 'Not found', 404
        if order.status != 'PAID':
            return 'Invalid parameters', 404

        replacement_id_in_a_list = self.validate_product_ids((replacement_id,))
        if len(replacement_id_in_a_list) == 0:
            return 'Invalid parameters', 400

        replacement_id = replacement_id_in_a_list[0]
        rows_affected = self.order_repository.insert_replacement_product(order_id, product_uuid, replacement_id,
                                                                         replacement_quantity)
        if rows_affected:
            self.connection.commit()
            return 'OK', 200
        else:
            self.connection.rollback()
        return None, None
