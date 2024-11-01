import os

# from apispec_webframeworks.flask import FlaskPlugin
# from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask, render_template, send_from_directory
from flasgger import APISpec, Swagger

from .config import ProductionConfig, DevelopmentConfig, TestingConfig
# from .schemas import UserSchema

APP_PATH: str = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH: str = os.path.join(APP_PATH, 'static')


def create_app(config_app=DevelopmentConfig):
    """
    Функция создания и настройки экземпляра приложения Flask

    :return app: экземпляр приложения
    :rtype app: Flask
    """

    app: Flask = Flask(
        __name__,
        instance_path=os.path.join(APP_PATH, '..', '..', 'instance'),
        instance_relative_config=True,
        template_folder=TEMPLATE_PATH
    )

    swagger_config = {
        "headers": [],
        "openapi": "3.0.1",
        "components": {
            'schemas': {
                'User': {
                    'title': 'User',
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'integer'
                        },
                        'name': {
                            'type': 'string'
                        }
                    }
                }
            }
        },
        "specs": [
            {
                "endpoint": "swagger",
                "route": "/apidocs/swagger.json",
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "title": "Tweet App Api",
        "version": '0.0.1',
        "termsOfService": "",
        "static_url_path": "/apidocs/static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
        "description": "",
    }

    swagger = Swagger(app, config=swagger_config)

    app.config.from_object(config_app) # конфигурация приложения

    # создание папки приложения
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # подключение модулей
    with app.app_context():
        from . import factories
        from . import database
        from . import models
        database.init_app(app)

    # регистрация blueprint
    from .routes import tweet, user, medias
    app.register_blueprint(tweet.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(medias.bp)

    @app.route('/')
    def index():
        """
        Роут отображения начальной страницы приложения

        :return: html страница
        :rtype: str
        """
        return render_template('index.html')

    @app.route('/<path:relative_link>')
    def download_file(relative_link: str):
        """
        Эндпоинт скачивания пользовательских файлов

        :param relative_link: относительный путь к файлу
        :type relative_link: str

        :return: HTTP ответ содержащий пользовательский файл, либо 'Not found' 404
        :rtype: Response
        """

        return send_from_directory(app.instance_path, relative_link)

    return app
