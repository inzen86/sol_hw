import os
import re
import tempfile

import pytest

from homework import create_app
from homework.db import get_connection, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture()
def app():
    db_file_dir, db_file_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_file_path
    })

    with app.app_context():
        init_db()
        get_connection().executescript(_data_sql)

    yield app

    os.close(db_file_dir)
    os.unlink(db_file_path)


@pytest.fixture()
def client(app):
    return app.test_client(use_cookies=False)


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_get_products(client):
    response = client.get('/api/products')
    expected = [
        {'id': 123, 'name': 'Ketchup', 'price': '0.45'},
        {'id': 456, 'name': 'Beer', 'price': '2.33'},
        {'id': 879, 'name': 'Õllesnäkk', 'price': '0.42'},
        {'id': 999, 'name': '75\" OLED TV', 'price': '1333.37'}
    ]
    assert response.json == expected


def test_create_new_order(client):
    response = client.post('/api/orders')
    expected_amount = {"discount": "0.00",
                       "paid": "0.00",
                       "returns": "0.00",
                       "total": "0.00"}
    uuid_regex = r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'

    assert response.json['amount'] == expected_amount
    assert re.match(uuid_regex, response.json['id'])
    assert response.json['products'] == []
    assert response.json['status'] == 'NEW'


def test_get_order(client):
    response = client.get('/api/orders/d4df8b90-8f4e-4fd5-bbf2-4dd6f366bb86')
    expected = {
        'amount': {
            'discount': '0.00',
            'paid': '0.00',
            'returns': '0.00',
            'total': '0.00'
        },
        'id': 'd4df8b90-8f4e-4fd5-bbf2-4dd6f366bb86',
        'products': [
            {'id': '4bacc3dd-30b7-4193-bc77-16d046804d54',
             'name': 'Ketchup',
             'price': '0.45',
             'product_id': 123,
             'quantity': 2,
             'replaced_with': []},
            {'id': '0248dfb0-d50c-4e37-a8b6-4d2d29d53a4d',
             'name': 'Beer',
             'price': '2.33',
             'product_id': 456,
             'quantity': 6,
             'replaced_with': []},
            {'id': '1d277343-0b0a-48db-b668-aa518b0bbc30',
             'name': 'Õllesnäkk',
             'price': '0.42',
             'product_id': 879,
             'quantity': 4,
             'replaced_with': []},
            {'id': '91941753-3f45-4742-89d4-755438a2a01f',
             'name': 'Ketchup',
             'price': '0.45',
             'product_id': 123,
             'quantity': 2,
             'replaced_with': {
                 'id': '5de14f8a-c49e-4dcd-b3b4-fe7ab9c6daa8',
                 'name': 'Beer',
                 'price': '2.33',
                 'product_id': 456,
                 'quantity': 3,
                 'replaced_with': []}}],
        'status': 'NEW'  # TODO: This is impossible in the original API, should be PAID before replacement can be added
    }
    assert response.json == expected
