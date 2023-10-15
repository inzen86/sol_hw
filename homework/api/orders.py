from flask import Blueprint, jsonify, abort, request

from homework.repository.setup_db import get_connection
from homework.service.orders_service import OrderService
from homework.service.products_service import ProductsService

bp = Blueprint('orders', __name__, url_prefix='/orders')


@bp.post('')
def create_and_get_order():
    connection = get_connection()
    order_service = OrderService(connection)
    response = jsonify(order_service.create_and_get())
    response.status_code = 201
    return response


@bp.get('<string:order_id>')
def get(order_id):
    connection = get_connection()
    order_service = OrderService(connection)
    order = order_service.get(order_id)
    if order is None:
        return not_found_404()
    return jsonify(order)


@bp.patch('<string:order_id>')
def update_stauts(order_id):
    connection = get_connection()
    order_service = OrderService(connection)

    if not len(request.data):
        return invalid_parameters_400()
    json = request.get_json(silent=True)
    if json is None:
        return bad_request_400()
    if not isinstance(json, dict):
        response = jsonify('Invalid order status')
        response.status_code = 400
        return response

    message, status_code = order_service.update_status(order_id, json.get('status'))
    if message is None or status_code is None:
        abort(500)
    response = jsonify(message)
    response.status_code = status_code
    return response


@bp.get('<string:order_id>/products')
def get_order_products(order_id):
    connection = get_connection()
    order_service = OrderService(connection)
    order_products = order_service.get_products_if_exists(order_id)
    if order_products is None:
        return not_found_404()
    return jsonify(order_products)


@bp.post('<string:order_id>/products')
def add_products(order_id):
    connection = get_connection()
    products_service = ProductsService(connection)
    order_service = OrderService(connection, products_service)

    if not len(request.data):
        return invalid_parameters_400()
    product_ids = request.get_json(silent=True)
    if product_ids is None:
        return bad_request_400()

    rows_affected = order_service.add_products(order_id, product_ids)

    if rows_affected:
        response = jsonify('OK')
        response.status_code = 201
    else:
        response = invalid_parameters_400()
    return response


@bp.patch('<string:order_id>/products/<string:product_uuid>')
def update_quantity_or_replace_product(order_id, product_uuid):
    connection = get_connection()
    products_service = ProductsService(connection)
    order_service = OrderService(connection, products_service)

    if not len(request.data):
        return invalid_parameters_400()
    parsed_json = request.get_json(silent=True)
    if parsed_json is None:
        return bad_request_400()
    if isinstance(parsed_json, dict) and not parsed_json:
        return invalid_parameters_400()

    quantity = parsed_json.get('quantity')
    replaced_with = parsed_json.get('replaced_with')

    message, status_code = None, None
    if quantity or quantity == 0:
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


def not_found_404():
    response = jsonify('Not found')
    response.status_code = 404
    return response


def invalid_parameters_400():
    response = jsonify('Invalid parameters')
    response.status_code = 400
    return response


def bad_request_400():
    response = jsonify({'errors': {'detail': 'Bad Request'}})
    response.status_code = 400
    return response
