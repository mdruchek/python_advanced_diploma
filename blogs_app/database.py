import click

from flask import current_app, g, Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base


engine = create_engine(current_app.config['DATABASE_URI'])
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


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database')


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
