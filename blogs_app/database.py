import click

from flask import current_app, g, Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from blogs_app import models
from blogs_app import factories


if current_app.config['ENVIRONMENT'] == 'dev':
    current_app.config['DATABASE'] = (
        current_app.config['DATABASE']
        .format(
            instance_path=current_app.instance_path,
        )
    )

engine = create_engine(current_app.config['DATABASE'], echo=current_app.config['ECHO_ENGINE_DATABASE'])
Session = sessionmaker(bind=engine)


def get_db():
    """
    Функиця возвращает экземпляр сессии

    :return: Сессия
    :rtype: Session
    """

    if 'db' not in g:
        g.db = Session()
    return g.db


def close_db(e=None):
    """
    Функция закрытия сессии
    """

    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    Функция инициализации базы данных для разработки
    """

    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    for _ in range(5):
        factories.UserFactory()
        factories.TweetFactory()


@click.command('init-dev-db')
def init_db_command():
    """
    Команда инициализации базы данных
    """

    init_db()
    click.echo('Initialized the database for development')


def init_app(app: Flask):
    """
    Инициализация приложения Flask

    :param app: экземпляр приложения
    :type app: Flask
    """

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
