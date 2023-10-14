from flask import Blueprint, jsonify, g
from flask import current_app as ca

from homework.api import orders, products
from homework.utils import gen_x_request_id

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.app_errorhandler(404)
def not_found(error):
    ca.logger.info(f'x-request-id: {g.x_request_id}, error: {error}')
    response = jsonify({"errors": {"detail": "Not Found"}})
    response.status_code = 404
    response.mimetype = 'application/json; charset=utf-8'
    return response


@bp.before_app_request
def add_x_request_id_to_g():
    # Adding x-request-id to g, so it could be used in endpoints.
    g.x_request_id = gen_x_request_id()


@bp.after_app_request
def add_x_request_id_to_response(response):
    response.headers['x-request-id'] = g.x_request_id
    return response


bp.register_blueprint(products.bp)
bp.register_blueprint(orders.bp)
