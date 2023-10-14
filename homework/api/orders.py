from flask import Blueprint, jsonify, abort, request

from homework.repository.setup_db import get_connection
from homework.service.orders_service import OrderService
from homework.service.products_service import ProductsService

bp = Blueprint('orders', __name__, url_prefix='/orders')


@bp.post('')
def create_and_get_order():
    connection = get_connection()
    order_service = OrderService(connection)
    return jsonify(order_service.create_and_get())


@bp.get('<string:order_id>')
def get_order(order_id):
    connection = get_connection()
    order_service = OrderService(connection)
    order = order_service.get(order_id)
    if order is None:
        response = jsonify('Not found')
        response.status_code = 404
        return response
    return jsonify(order)


@bp.patch('<string:order_id>')
def update_order(order_id):
    connection = get_connection()
    order_service = OrderService(connection)
    message, status_code = order_service.update_status(order_id, request.json['status'])
    if message is None or status_code is None:
        abort(500)
    response = jsonify(message)
    response.status_code = status_code
    return response


@bp.get('<string:order_id>/products')
def get_order_products(order_id):
    connection = get_connection()
    order_service = OrderService(connection)
    order_products = order_service.get_products(order_id)
    if order_products is None:
        response = jsonify('Not found')
        response.status_code = 404
        return response
    return jsonify(order_products)


@bp.post('<string:order_id>/products')
def add_product_to_order(order_id):
    connection = get_connection()
    products_service = ProductsService(connection)
    order_service = OrderService(connection, products_service)

    if len(request.data) < 1:
        response = jsonify('Invalid parameters')
        response.status_code = 400
        return response

    product_ids = request.get_json(silent=True)
    if not product_ids:  # json was not parsable
        response = jsonify({'errors': {'detail': 'Bad Request'}})
        response.status_code = 400
        return response

    rows_affected = order_service.add_products(order_id, product_ids)

    if rows_affected:
        response = jsonify('OK')
        response.status_code = 201
    else:
        response = jsonify('Invalid parameters')
        response.status_code = 400
    return response


@bp.patch('<string:order_id>/products/<string:product_uuid>')
def update_quantity_or_replace_product(order_id, product_uuid):
    connection = get_connection()
    products_service = ProductsService(connection)
    order_service = OrderService(connection, products_service)

    if not len(request.data):
        response = jsonify('Invalid parameters')
        response.status_code = 400
        return response

    parsed_json = request.get_json(silent=True)
    if not parsed_json:  # json was not parsable
        response = jsonify({'errors': {'detail': 'Bad Request'}})
        response.status_code = 400
        return response

    quantity = parsed_json.get('quantity')
    replaced_with = parsed_json.get('replaced_with')

    message, status_code = None, None
    if quantity:
        message, status_code = order_service.update_quantity(order_id, product_uuid, quantity)
    elif replaced_with:
        replacement_id = replaced_with.get('product_id')
        replacement_quantity = replaced_with.get('quantity')

        message, status_code = order_service.replace_product(order_id, product_uuid, replacement_id,
                                                             replacement_quantity)
    if message is None or status_code is None:
        abort(500)
    response = jsonify(message)
    response.status_code = status_code

    return response
