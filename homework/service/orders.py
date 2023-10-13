import sqlite3
from uuid import uuid4


def create_new_order(con):
    order_id = str(uuid4())
    con.execute('''insert into orders (id) values (?)''',
                (order_id,))
    return order_id


def get_order_from_db(con, order_id):
    row = con.execute('select id, status, discount, paid, returns, 0.0 as total from orders where id = ?',
                      (order_id,)).fetchone()
    if row is None:
        return None

    order_items = get_order_items_from_db(con, order_id)
    if order_items is None:
        order_items = []

    return {
        "amount": {
            "discount": f"{row['discount']:.2f}",
            "paid": f"{row['paid']:.2f}",
            "returns": f"{row['returns']:.2f}",
            "total": f"{row['returns']:.2f}"},
        "id": f"{row['id']}",
        "products": order_items,
        "status": f"{row['status']}"
    }


def get_order_items_from_db(con, order_id):
    query = '''
        select oi.id,
               p.name,
               p.price,
               oi.product_id,
               oi.quantity,
               r.id as r_id,
               rp.name as r_name,
               rp.price as r_price,
               rp.id as r_product_id,
               r.quantity as r_quantity
        from order_items as oi
        join products as p on oi.product_id = p.id
        left join replacements as r on oi.id = r.original_id
        left join products as rp on r.product_id = rp.id
        where oi.order_id = ?
        '''

    cur = con.execute(query, (order_id,)).fetchall()

    if cur is None:
        return

    products = []
    for row in cur:
        order_item = {
            "id": row['id'],
            "name": row['name'],
            "price": f"{row['price']:.2f}",
            "product_id": row['product_id'],
            "quantity": row['quantity'],
            "replaced_with": []
        }

        if row['r_id'] is not None:
            order_item['replaced_with'] = {
                "id": row['r_id'],
                "name": row['r_name'],
                "price": f"{row['r_price']:.2f}",
                "product_id": row['r_product_id'],
                "quantity": row['r_quantity'],
                "replaced_with": []
            }

        products.append(order_item)

    return products


def update_order_status(con, order_id, requested_status):
    # Currently only supports changing NEW to PAID

    row = con.execute('select status from orders where id = ?', (order_id,)).fetchone()
    if row is None:
        return 'Not found', 404

    # These should be separate if-s, but currently this matches reference API
    if row['status'] != 'NEW' or requested_status != 'PAID':
        return 'Invalid order status', 400

    if row['status'] == 'NEW' and requested_status == 'PAID':
        cur = con.execute("update orders set status = 'PAID' where id = ?", (order_id,))
        if cur.rowcount == 1:
            con.commit()
            return 'OK', 200

    return None, None


def get_order_products(con, order_id):
    order_exists = con.execute('select 1 from orders where id = ?', (order_id,)).fetchone()
    if order_exists is None:
        return
    return get_order_items_from_db(con, order_id)
