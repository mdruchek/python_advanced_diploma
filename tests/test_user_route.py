from sqlalchemy import select, func

from blogs_app.models import Follow, User
from .functions import checking_by_api_error_type

def test_create_follow(client, user):
    # запрос с некорректным api_key
    response = client.post('/api/users/1/follow', headers={'Api-Key': 'no_valid_api_key'})
    json_data = response.get_json()
    checking_by_api_error_type(
        json_data=json_data,
        error_type='Forbidden',
        error_message=f'Access is denied. User with api-key no_valid_api_key not found'
    )

    # попытка подписаться на несуществующего автора
    no_found_author_number = 9999
    response = client.post(f'/api/users/{no_found_author_number}/follow', headers={'Api-Key': user.api_key})
    assert response.status_code == 404
    json_data = response.get_json()
    checking_by_api_error_type(
        json_data=json_data,
        error_type='Not found',
        error_message=f'Author with id={no_found_author_number} not found'
    )

    # попытка подписаться на себя
    response = client.post(f'/api/users/{user.id}/follow', headers={'Api-Key': user.api_key})
    assert response.status_code == 403
    json_data = response.get_json()
    checking_by_api_error_type(
        json_data=json_data,
        error_type='Forbidden',
        error_message='The user cannot follow himself'
    )

    # подписка на автора номер 1
    response = client.post(f'/api/users/1/follow', headers={'Api-Key': user.api_key})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['result'] is True

def test_delete_follow(session, client, user):
    # запрос с некорректным api_key
    response = client.delete('/api/users/1/follow', headers={'Api-Key': 'no_valid_api_key'})
    json_data = response.get_json()
    checking_by_api_error_type(
        json_data=json_data,
        error_type='Forbidden',
        error_message=f'Access is denied. User with api-key no_valid_api_key not found'
    )

    # попытка удалить подписку на несуществующего автора
    no_found_author_number = 9999
    response = client.delete(f'/api/users/{no_found_author_number}/follow', headers={'Api-Key': user.api_key})
    assert response.status_code == 404
    json_data = response.get_json()
    checking_by_api_error_type(
        json_data=json_data,
        error_type='Not found',
        error_message=f'Author with id={no_found_author_number} not found'
    )

    # попытка удалить подписку с себя
    response = client.delete(f'/api/users/{user.id}/follow', headers={'Api-Key': user.api_key})
    assert response.status_code == 403
    json_data = response.get_json()
    checking_by_api_error_type(
        json_data=json_data,
        error_type='Forbidden',
        error_message='The user cannot unfollow himself'
    )

    # подписка и удаление подписки с автора номер 1
    follow = Follow(author_id=1, follower_id=user.id)
    session.add(follow)
    session.commit()
    user = session.get(User, 6)
    assert len(user.follows_author) == 1
    response = client.delete(f'/api/users/1/follow', headers={'Api-Key': user.api_key})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['result'] is True
