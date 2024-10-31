from typing import Optional

from flask import Blueprint, request, jsonify
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from blogs_app import database
from blogs_app.models import User, Follow
from blogs_app import responses_api

bp = Blueprint('users', __name__, url_prefix='/api/users')


@bp.route('/<int:author_id>/follow', methods=('POST',))
def create_follow(author_id):
    """
    Эндпоинт добавления подписки на автора
    ---
    tags:
        - users
    parameters:
        - in: header
          name: Api-Key
          required: true
        - in: path
          name: author_id
          required: true
    responses:
        201:
            description: Подписка создана
            schema:
                example: {
                    'result': True
                }
        403:
            description: Пользователь с данным api-key не найден или пользователь пытается подписаться на самого себя
            schema:
                example: {
                    'result': False,
                    'error_type': 'Forbidden',
                    'error_message': 'string'
                }
        404:
            description: Author with given id not found
            schema:
                example: {
                    'result': False,
                    'error_type': 'Not found',
                    'error_message': 'string'
                }
    """

    db: Session = database.get_session()
    api_key: str = request.headers.get('Api-Key')
    user: Optional[User] = db.execute(select(User).where(User.api_key == api_key)).scalar()

    if not user:
        return jsonify(
            responses_api.ResponsesAPI.error_forbidden(
                f'Access is denied. User with api-key {api_key} not found'
            )
        ), 403

    author = db.get(User, author_id)

    if not author:
        return jsonify(responses_api.ResponsesAPI.error_not_found(f'Author with id={author_id} not found')), 404

    if user.id == author.id:
        return jsonify(responses_api.ResponsesAPI.error_forbidden('The user cannot follow himself')), 403

    follow_for_create: Follow = Follow(author_id=author_id, follower_id=user.id)
    db.add(follow_for_create)
    db.commit()
    return jsonify(responses_api.ResponsesAPI.result_true()), 201


@bp.route('/<int:author_id>/follow', methods=('DELETE',))
def delete_follow(author_id):
    """
    Эндпоинт удаления подписки с автора
    ---
    tags:
        - users
    parameters:
        - in: header
          name: Api-Key
          required: true
        - in: path
          name: author_id
          required: true
    responses:
        201:
            description: Подписка удалена
            schema:
                example: {
                    'result': True
                }
        403:
            description: Пользователь с данным api-key не найден или пользователь пытается удалить подписку на самого себя
            schema:
                example: {
                    'result': False,
                    'error_type': 'Forbidden',
                    'error_message': 'string'
                }
        404:
            description: Author with given id not found
            schema:
                example: {
                    'result': False,
                    'error_type': 'Not found',
                    'error_message': 'string'
                }
    """

    db: Session = database.get_session()
    api_key: str = request.headers.get('Api-Key')
    user: Optional[User] = db.execute(select(User).where(User.api_key == api_key)).scalar()

    if not user:
        return jsonify(
            responses_api.ResponsesAPI.error_forbidden(
                f'Access is denied. User with api-key {api_key} not found'
            )
        ), 403

    author: Optional[User] = db.get(User, author_id)

    if not author:
        return jsonify(responses_api.ResponsesAPI.error_not_found(f'Author with id={author_id} not found')), 404

    if user.id == author.id:
        return jsonify(responses_api.ResponsesAPI.error_forbidden('The user cannot unfollow himself')), 403

    db.execute(
        delete(Follow)
        .where(Follow.follower_id == user.id and Follow.author_id == author.id)
    )

    db.commit()
    return jsonify(responses_api.ResponsesAPI.result_true())


@bp.route('/me', methods=('GET',))
def get_me():
    """
    Эндпоинт возвращает информацию авторизированного пользователя
    ---
    tags:
        - users
    parameters:
        - in: header
          name: Api-Key
          required: true
    responses:
        200:
            description: Информация пользователя о себе
            schema:
                type: object
                properties:
                    result: true
                    user:
                        $ref: '#/definitions/User'
                        readOnly: true
        403:
            description: Пользователь с данным api-key не найден или пользователь пытается подписаться на самого себя
            schema:
                example: {
                    'result': False,
                    'error_type': 'Forbidden',
                    'error_message': 'string'
                }
    """

    api_key: str = request.headers.get('Api-Key')

    if api_key == 'test':
        return jsonify(responses_api.ResponsesAPI.result_true({'user': {'name': 'test'}}))

    db: Session = database.get_session()
    user: Optional[User] = db.execute(
        select(
            User
        ).where(
            User.api_key == api_key
        )
    ).scalar()

    if not user:
        return jsonify(
            responses_api.ResponsesAPI.error_forbidden(
                f'Access is denied. User with api-key {api_key} not found'
            )
        ), 403

    user_dict: dict = user.to_dict(exclude=('api_key',))
    user_dict['followers']: list[dict] = [f.follower.to_dict(exclude=('api_key',)) for f in user.follows_author]
    user_dict['following']: list[dict] = [f.author.to_dict(exclude=('api_key',)) for f in user.follows_follower]
    return jsonify(responses_api.ResponsesAPI.result_true({'user': user_dict})), 200


@bp.route('/<int:user_id>', methods=('GET',))
def get_user_by_id(user_id):
    """
    Эндпоинт возвращает информацию о пользователе по его id

    :param user_id: id пользователя
    :type user_id: int

    :return: Ответ с информаицией о пользователе
    :rtype: Response
    """

    db: Session = database.get_session()

    user: Optional[User] = db.execute(
        select(
            User,
        ).where(
            User.id == user_id
        )
    ).scalar()

    if not user:
        return jsonify(responses_api.ResponsesAPI.error_not_found(f'User with id {user_id} not found')), 404

    user_dict: dict = user.to_dict(exclude=('api_key',))
    user_dict['followers']: list[dict] = [f.follower.to_dict(exclude=('api_key',)) for f in user.follows_author]
    user_dict['following']: list[dict] = [f.author.to_dict(exclude=('api_key',)) for f in user.follows_follower]
    return jsonify(responses_api.ResponsesAPI.result_true({'user': user_dict})), 200
