import os

from flask import Flask, Response
from flask.json.provider import DefaultJSONProvider
from flask.typing import t

from homework.repository import setup_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, static_folder=None)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite')
    )

    app.json_provider_class = CustJSONProvider

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from homework.api import main
    app.register_blueprint(main.bp)

    from homework.repository import setup_db
    setup_db.init_app(app)

    return app


class CustJSONProvider(DefaultJSONProvider):
    def response(self, *args: t.Any, **kwargs: t.Any) -> Response:
        obj = self._prepare_response_obj(args, kwargs)

        return self._app.response_class(
            self.dumps(obj, ensure_ascii=False),
            mimetype='application/json; charset=utf-8'
        )
