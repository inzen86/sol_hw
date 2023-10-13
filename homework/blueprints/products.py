from flask import jsonify, Blueprint

from homework.db.db import get_connection
from homework.service.products import get_products_from_db

bp = Blueprint('products', __name__, url_prefix='/products')


@bp.route('')
def get_products():
    con = get_connection()
    return jsonify(get_products_from_db(con))
