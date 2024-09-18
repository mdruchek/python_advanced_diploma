import click

from flask import current_app, g, Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base


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
    if 'db' not in g:
        g.db = Session()
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@click.command('init-dev-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database for development')


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
