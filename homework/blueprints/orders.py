from flask import Blueprint, jsonify, abort, request, current_app

from homework.db.db import get_connection
from homework.service import orders as o

bp = Blueprint('orders', __name__, url_prefix='/orders')


@bp.post('')
def create_and_get_order():
    con = get_connection()
    order_id = o.create_new_order(con)
    con.commit()
    return jsonify(o.get_order_from_db(con, order_id))


@bp.get('<string:order_id>')
def get_order(order_id):
    con = get_connection()
    order = o.get_order_from_db(con, order_id)
    if order is None:
        response = jsonify('Not found')
        response.status_code = 404
        return response
    return jsonify(order)


@bp.patch('<string:order_id>')
def update_order(order_id):
    con = get_connection()

    msg, code = o.update_order_status(con, order_id, request.json['status'])
    if msg is None or code is None:
        abort(500)
    response = jsonify(msg)
    response.status_code = code
    return response


@bp.get('<string:order_id>/products')
def get_order_products(order_id):
    con = get_connection()
    items = o.get_order_products(con, order_id)
    if items is None:
        response = jsonify('Not found')
        response.status_code = 404
        return response
    return jsonify(items)


@bp.post('<string:order_id>/products')
def add_product_to_order(order_id):
    # does order exist?
    # is order status correct? 'NEW'
    # does item exist
    # product_ids are a list
    current_app.logger.debug(f'json: {request.get_json(silent=True)}')
    return 'Hi'
