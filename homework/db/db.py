import sqlite3

import click
import flask
from flask import current_app, g


def get_connection():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_connection(e=None):  # TODO: Not sure where e will be used, probably when closing connection due to error.
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_connection()

    with current_app.open_resource('db/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    with current_app.open_resource('db/initial_products.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database')


def init_app(app: flask.Flask):
    app.teardown_appcontext(close_connection)
    app.cli.add_command(init_db_command)
