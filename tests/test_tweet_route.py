from flask import Response
from sqlalchemy import select, insert, func

from blogs_app.models import Tweet, Like
from .functions import checking_by_api_error_type


def test_create_tweet(client, session, user):
    request_url: str = '/api/tweets/'
    request_data: dict = {
        'tweet_data': 'Test tweet',
        'tweet_media_ids': []
    }

    number_of_tweets_in_database: int = session.execute(select(func.count(Tweet.id))).scalar()

    # запрос с некорректным api_key
    response: Response = client.post(request_url, json=request_data, headers={'Api-Key': 'no_valid_api_key'})
    assert response.status_code == 403
    json_data: dict = response.get_json()
    checking_by_api_error_type(
        json_data=json_data,
        error_type='Forbidden',
        error_message='Access is denied. User with api-key no_valid_api_key not found'
    )

    # запрос с корректным api_key
    response: Response = client.post(request_url, json=request_data, headers={'Api-Key': user.api_key})
    assert response.status_code == 200
    json_data: dict = response.get_json()
    assert json_data['result'] is True
    assert json_data['tweet_id'] == number_of_tweets_in_database + 1


def test_delete_tweet(client, tweet):
    # запрос с некорректным api_key
    response: Response = client.delete('/api/tweets/1', headers={'Api-Key': 'no_valid_api_key'})
    assert response.status_code == 403
    json_data: dict = response.get_json()
    checking_by_api_error_type(
        json_data=json_data,
        error_type='Forbidden',
        error_message='Access is denied. User with api-key no_valid_api_key not found'
    )

    # запрос с несуществующим tweet_id
    no_found_tweet_number: int = 9999
    response = client.delete(f'/api/tweets/{no_found_tweet_number}', headers={'Api-Key': tweet.author.api_key})
    assert response.status_code == 404
    json_data: dict = response.get_json()
    checking_by_api_error_type(
        json_data=json_data,
        error_type='Not found',
        error_message=f'Tweet with id={no_found_tweet_number} not found')

    # попытка удалить чужой твит
    response: Response = client.delete('/api/tweets/1', headers={'Api-Key': tweet.author.api_key})
    assert response.status_code == 403
    json_data: dict = response.get_json()
    checking_by_api_error_type(
        json_data=json_data,
        error_type='Forbidden',
        error_message='User can only delete their own blogs'
    )

    # удаление своего твита
    response: Response = client.delete(f'/api/tweets/{tweet.id}', headers={'Api-Key': tweet.author.api_key})
    assert response.status_code == 200
    json_data: dict = response.get_json()
    assert json_data['result'] is True


def test_create_like(session, client, tweet):
    tweet_1: Tweet = session.execute(select(Tweet).where(Tweet.id == 1)).scalar()
    assert isinstance(tweet_1.likes, list)
    assert not tweet_1.likes

    # запрос с некорректным api_key
    response: Response = client.post(f'/api/tweets/{tweet_1.id}/likes', headers={'Api-Key': 'no_valid_api_key'})
    assert response.status_code == 403
    json_data: dict = response.get_json()
    checking_by_api_error_type(
        json_data=json_data,
        error_type='Forbidden',
        error_message='Access is denied. User with api-key no_valid_api_key not found'
    )

    # запрос с несуществующим tweet_id
    no_found_tweet_number: int = 9999
    response: Response = client.post(f'/api/tweets/{no_found_tweet_number}/likes', headers={'Api-Key': tweet.author.api_key})
    assert response.status_code == 404
    json_data: dict = response.get_json()
    checking_by_api_error_type(
        json_data=json_data,
        error_type='Not found',
        error_message=f'Tweet with id={no_found_tweet_number} not found')

    # попытка поставить лайк на свой твит
    response: Response = client.post(f'/api/tweets/{tweet.id}/likes', headers={'Api-Key': tweet.author.api_key})
    assert response.status_code == 403
    json_data: dict = response.get_json()
    checking_by_api_error_type(
        json_data=json_data,
        error_type='Forbidden',
        error_message=f"You can only like other people's tweets")

    # лайк чужого твита
    response: Response = client.post(f'/api/tweets/{tweet_1.id}/likes', headers={'Api-Key': tweet.author.api_key})
    assert response.status_code == 200
    json_data: dict = response.get_json()
    assert json_data['result'] is True
    assert tweet_1.likes


def test_delete_like(session, client, user):
    # запрос с некорректным api_key
    response: Response = client.delete(f'/api/tweets/1/likes', headers={'Api-Key': 'no_valid_api_key'})
    assert response.status_code == 403
    json_data: dict = response.get_json()
    checking_by_api_error_type(
        json_data=json_data,
        error_type='Forbidden',
        error_message='Access is denied. User with api-key no_valid_api_key not found'
    )

    # удаление поставленного лайка
    session.execute(insert(Like).values(user_id=user.id, tweet_id=1))
    session.commit()
    response: Response = client.delete('/api/tweets/1/likes', headers={'Api-Key': user.api_key})
    assert response.status_code == 200
    json_data: dict = response.get_json()
    assert json_data['result'] is True


def test_get_tweets(client, tweet):
    response: Response = client.get('/api/tweets/')
    assert response.status_code == 200
    json_data: dict = response.get_json()
    assert json_data['result'] is True
    assert 'tweets' in json_data
    assert isinstance(json_data['tweets'], list)
    test_tweet: dict = json_data['tweets'][0]
    assert test_tweet == {
        'id': 6,
        'author': {
            'id': 6,
            'name': 'test_user'
        },
        'content': 'test_tweet_content',
        'likes': []
    }
