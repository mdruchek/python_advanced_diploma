import os

from flask import Flask, render_template

from .config import ProductionConfig


APP_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(APP_PATH, 'static')


def create_app():

    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=TEMPLATE_PATH
    )

    app.config.from_object(ProductionConfig)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import database
    database.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
