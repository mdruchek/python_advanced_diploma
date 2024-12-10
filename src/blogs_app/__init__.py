"""blogs_app."""

import os

from flasgger import Swagger
from flask import Flask, Response, render_template, send_from_directory

from blogs_app.config import DevelopmentConfig

APP_PATH: str = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH: str = os.path.join(APP_PATH, 'static')


def create_app(config_app=DevelopmentConfig):
    """Функция создания и настройки экземпляра приложения Flask.

    Parameters:
        config_app: конфигурация приложения

    Returns:
        app: экземпляр приложения
    """
    app: Flask = Flask(
        __name__,
        instance_path=os.path.join(APP_PATH, '..', '..', 'instance'),
        instance_relative_config=True,
        template_folder=TEMPLATE_PATH,
    )

    swagger_config = {
        'headers': [],
        'openapi': '3.0.1',
        'components': {
            'schemas': {
                'User': {
                    'title': 'User',
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'integer',
                        },
                        'name': {
                            'type': 'string',
                            'example': 'Username',
                        },
                    },
                },
                'Tweet': {
                    'title': 'Tweet',
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'integer',
                        },
                        'content': {
                            'type': 'string',
                            'example': 'Content tweet',
                        },
                        'attachments': {
                            'type': 'array',
                            'items': {
                                'type': 'string',
                                'example': '/link/on/media',
                            },
                        },
                        'author': {
                            '$ref': '#/components/schemas/User',
                        },
                        'likes': {
                            'type': 'array',
                            'items': {
                                'properties': {
                                    'user_id': {
                                        'type': 'integer',
                                    },
                                    'name': {
                                        'type': 'string',
                                        'example': 'Username',
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        'specs': [
            {
                'endpoint': 'swagger',
                'route': '/apidocs/swagger.json',
                'rule_filter': lambda rule: True,  # all in
                'model_filter': lambda tag: True,  # all in
            },
        ],
        'title': 'Tweet App Api',
        'version': '0.0.1',
        'termsOfService': '',
        'static_url_path': '/apidocs/static',
        'swagger_ui': True,
        'specs_route': '/apidocs/',
        'description': '',
    }

    swagger = Swagger(app, config=swagger_config)

    app.config.from_object(config_app)  # конфигурация приложения

    # создание папки приложения
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # подключение модулей
    with app.app_context():
        from blogs_app import database, factories, models
        database.init_app(app)

    # регистрация blueprint
    from blogs_app.routes import medias, tweet, user
    app.register_blueprint(tweet.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(medias.bp)

    @app.route('/')
    def index():
        """Роут отображения начальной страницы приложения.

        Returns:
            html страница
        """
        return render_template('index.html')

    @app.route('/<path:relative_link>')
    def download_file(relative_link: str) -> Response:
        """Эндпоинт скачивания пользовательских файлов.

        Parameters:
            relative_link: относительный путь к файлу

        Returns:
            HTTP ответ содержащий пользовательский файл, либо 'Not found' 404
        """
        return send_from_directory(app.instance_path, relative_link)

    return app
