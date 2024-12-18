"""База данных."""

import click
from flask import Flask, current_app, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from blogs_app import models

if not current_app.config['TESTING'] and current_app.config['ENVIRONMENT'] == 'dev':
    current_app.config['DATABASE'] = (
        current_app.config['DATABASE'].format(
            instance_path=current_app.instance_path,
        )
    )

engine = create_engine(current_app.config['DATABASE'], echo=current_app.config['ECHO_ENGINE_DATABASE'])
Session = sessionmaker(bind=engine)


def get_session():
    """Функиця возвращает экземпляр сессии.

    Returns:
        Сессия
    """
    if 'db' not in g:
        g.db = Session()
    return g.db


def close_session(exc=None):
    """Функция закрытия сессии.

    Parameters:
        exc: исключения
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Функция инициализации базы данных для разработки."""
    from blogs_app import factories

    drop_all_models_from_db()
    models.Base.metadata.create_all(bind=engine)
    for _ in range(5):
        factories.UserFactory()
        factories.TweetFactory()


def drop_all_models_from_db():
    """Удаляет таблицы базы данных."""
    models.Base.metadata.drop_all(bind=engine)


@click.command('init-dev-db')
def init_db_command():
    """Команда инициализации базы данных."""
    init_db()
    click.echo('Initialized the database for development')


def init_app(app: Flask):
    """Инициализация приложения Flask.

    Parameters:
        app: экземпляр приложения
    """
    app.teardown_appcontext(close_session)
    app.cli.add_command(init_db_command)
