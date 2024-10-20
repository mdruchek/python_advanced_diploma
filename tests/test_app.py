from select import select

import pytest
from sqlalchemy import select, func

from blogs_app.models import Tweet


def test_app_config(app):
    assert app.config['TESTING']
    assert app.config['DATABASE'] == 'sqlite:///:memory:'


@pytest.mark.parametrize('route', ['/api/tweets/', '/api/users/1'])
def test_get_route_status(client, route):
    result = client.get(route)
    assert result.status_code == 200


def test_init_dev_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_dev_db():
        Recorder.called = True

    monkeypatch.setattr('blogs_app.database.init_db', fake_init_dev_db)
    result = runner.invoke(args=['init-dev-db'])
    assert 'Initialized' in result.output
    assert Recorder.called


def test_create_tweet(client, request, session):
    request_url: str = '/api/tweets/'
    request_data = {
        'tweet_data': 'Test tweet',
        'tweet_media_ids': []
    }

    number_of_tweets_in_database = session.execute(select(func.count(Tweet.id))).scalar()
    request_headers = {'Api-Key': 'valid_api_key'}
    response = client.post(request_url, json=request_data, headers=request_headers)
    assert response.status_code == 403

    request.getfixturevalue('create_test_user')
    response = client.post(request_url, json=request_data, headers=request_headers)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['result'] is True
    assert json_data['tweet_id'] == number_of_tweets_in_database + 1


def test_delete_tweet(client, create_test_user):
    response = client.delete('/api/tweets/1', headers={'Api-Key': 'valid_api_key'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['result'] is True


def test_get_tweets(client, create_test_user):
    response = client.get('/api/tweets/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['result'] is True


def test_delete_like(client, create_test_user):
    response = client.delete('/api/tweets/1/like', headers={'Api-Key': 'valid_api_key'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['result'] is True
