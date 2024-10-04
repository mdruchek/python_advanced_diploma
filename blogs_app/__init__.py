import os

from flask import Flask, render_template, send_from_directory

from .config import ProductionConfig, DevelopmentConfig


APP_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(APP_PATH, 'static')


def create_app():

    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=TEMPLATE_PATH
    )

    app.config.from_object(DevelopmentConfig())

    with app.app_context():
        from . import factories
        from . import database
        from . import models

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from . import database
        database.init_app(app)

    from .routes import tweet, user, medias
    app.register_blueprint(tweet.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(medias.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/uploads/<path:file_name>')
    def download_file(file_name: str):
        return send_from_directory('', file_name.replace('\\', '/'))

    return app
