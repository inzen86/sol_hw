import sqlite3

import click
from flask import current_app, g, Flask


def get_connection() -> sqlite3.Connection:
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_connection(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db(app):
    with app.app_context():
        db = get_connection()

        tables_exist = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'").fetchone()
        if tables_exist:
            return

        click.echo('Initializing database')
        with current_app.open_resource('repository/schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
        with current_app.open_resource('repository/initial_products.sql') as f:
            db.executescript(f.read().decode('utf8'))
        click.echo('database ready')


def init_app(app: Flask):
    init_db(app)
    app.teardown_appcontext(close_connection)
