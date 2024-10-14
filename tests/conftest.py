import pytest

from blogs_app import create_app
from blogs_app.config import TestingConfig



@pytest.fixture
def app():
    _app = create_app(config_app=TestingConfig)
    with _app.app_context():
        from blogs_app.database import init_db, drop_all_models_from_db
    init_db()

    yield _app

    drop_all_models_from_db()


@pytest.fixture
def db(app):
    with app.app_context():
        from blogs_app.database import get_db
        yield get_db()


@pytest.fixture
def web_client(app):
    client = app.test_client()
    return client
