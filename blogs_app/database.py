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
    Base.metadata.create_all(bind=engine)


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
