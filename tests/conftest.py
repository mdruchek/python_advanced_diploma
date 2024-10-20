import pytest

from blogs_app import create_app
from blogs_app.config import TestingConfig
from blogs_app.models import User, Tweet


@pytest.fixture
def app():
    _app = create_app(config_app=TestingConfig)
    with _app.app_context():
        from blogs_app.database import init_db
        init_db()

    yield _app

    with _app.app_context():
        from blogs_app.database import drop_all_models_from_db
        drop_all_models_from_db()


@pytest.fixture
def session(app):
    with app.app_context():
        from blogs_app.database import get_session

        yield get_session()

    with app.app_context():
        from blogs_app.database import close_session
        close_session()


@pytest.fixture
def client(app):
    client = app.test_client()
    return client


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def user(session):
    test_user = User(name="test_user", api_key="valid_api_key")
    session.add(test_user)
    session.commit()
    return test_user


@pytest.fixture
def tweet(session, user):
    test_tweet = Tweet(content='test_tweet_content', author_id = user.id)
    session.add(test_tweet)
    session.commit()
    return test_tweet
