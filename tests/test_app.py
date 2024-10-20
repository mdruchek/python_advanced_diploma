from select import select

import pytest
from sqlalchemy import select, func

from blogs_app.models import Tweet


def test_app_config(app):
    assert app.config['TESTING']
    assert app.config['DATABASE'] == 'sqlite:///:memory:'


def test_init_dev_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_dev_db():
        Recorder.called = True

    monkeypatch.setattr('blogs_app.database.init_db', fake_init_dev_db)
    result = runner.invoke(args=['init-dev-db'])
    assert 'Initialized' in result.output
    assert Recorder.called


def test_create_tweet(client, request, session, user):
    request_url: str = '/api/tweets/'
    request_data = {
        'tweet_data': 'Test tweet',
        'tweet_media_ids': []
    }

    number_of_tweets_in_database = session.execute(select(func.count(Tweet.id))).scalar()

    response = client.post(request_url, json=request_data, headers={'Api-Key': 'no_valid_api_key'})
    assert response.status_code == 403
    json_data = response.get_json()
    assert json_data['result'] is False
    assert json_data['error_type'] == 'Forbidden'
    assert json_data['error_message'] == 'Access is denied. User with api-key no_valid_api_key not found'

    response = client.post(request_url, json=request_data, headers={'Api-Key': 'valid_api_key'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['result'] is True
    assert json_data['tweet_id'] == number_of_tweets_in_database + 1


def test_delete_tweet(client, tweet):
    response = client.delete('/api/tweets/1', headers={'Api-Key': 'no_valid_api_key'})
    assert response.status_code == 403
    json_data = response.get_json()
    assert json_data['result'] is False
    assert json_data['error_type'] == 'Forbidden'
    assert json_data['error_message'] == 'Access is denied. User with api-key no_valid_api_key not found'

    no_found_tweet_number = 9999
    response = client.delete(f'/api/tweets/{no_found_tweet_number}', headers={'Api-Key': 'valid_api_key'})
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data['result'] is False
    assert json_data['error_type'] == 'Not found'
    assert json_data['error_message'] == f'Tweet with id={no_found_tweet_number} not found'

    response = client.delete('/api/tweets/1', headers={'Api-Key': 'valid_api_key'})
    assert response.status_code == 403
    json_data = response.get_json()
    assert json_data['result'] is False
    assert json_data['error_type'] == 'Forbidden'
    assert json_data['error_message'] == 'User can only delete their own blogs'

    response = client.delete(f'/api/tweets/{tweet.id}', headers={'Api-Key': 'valid_api_key'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['result'] is True


def test_get_tweets(client, user):
    response = client.get('/api/tweets/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['result'] is True


def test_delete_like(client, user):
    response = client.delete('/api/tweets/1/like', headers={'Api-Key': 'valid_api_key'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['result'] is True
