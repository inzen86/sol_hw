def get_products_from_db(con):
    # Get products from the database and create dict with same structure as expected json
    rows = con.execute('select id, name, price from products order by id').fetchall()
    products = []

    for row in rows:
        products.append({'id': row['id'],
                         'name': row['name'],
                         'price': str(row['price'])})
    return products
