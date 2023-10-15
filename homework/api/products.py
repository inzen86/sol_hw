from flask import jsonify, Blueprint

from homework.repository.setup_db import get_connection
from homework.service.products_service import ProductsService

bp = Blueprint('products', __name__, url_prefix='/products')


@bp.get('')
def get_products():
    connection = get_connection()
    products_service = ProductsService(connection)
    products = products_service.get()
    return jsonify(products)
