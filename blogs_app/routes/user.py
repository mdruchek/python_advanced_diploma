from flask import Blueprint, request, jsonify
from sqlalchemy import select

from blogs_app import database
from blogs_app.models import User, Follow
from blogs_app import responses_api

bp = Blueprint('users', __name__, url_prefix='/api/users')


@bp.route('/<int:author_id>/follow', methods=('POST',))
def create_follow(author_id):
    db = database.get_db()
    api_key = request.headers.get('Api-Key')
    user = db.execute(select(User).where(User.api_key == api_key)).scalar()
    author = db.get(User, author_id)
    if not author:
        return jsonify(responses_api.ResponsesAPI.error_not_found(f"Author with id={author_id} not found")), 404
    if user.id == author.id:
        return jsonify(responses_api.ResponsesAPI.error_forbidden("The user cannot follow himself")), 403

    follow_for_create = Follow(author_id=author_id, follower=user.id)
    db.add(follow_for_create)
    db.commit()
    return jsonify(responses_api.ResponsesAPI.result_true())


@bp.route('/<int:author_id>/follow', methods=('DELETE',))
def delete_follow(author_id):
    db = database.get_db()
    api_key = request.headers.get('Api-Key')
    user = db.execute(select(User).where(User.api_key == api_key)).scalar()
    author = db.get(User, author_id)

    if not author:
        return jsonify(responses_api.ResponsesAPI.error_not_found(f"Author with id={author_id} not found")), 404

    if user.id == author.id:
        return jsonify(responses_api.ResponsesAPI.error_forbidden("The user cannot unfollow himself")), 403

    follow_for_delete = db.execute(
        select(
            Follow
        )
        .where(
            Follow.follower_id == user.id
            and Follow.author_id == author.id
        )
    ).scalar()

    db.delete(follow_for_delete)
    db.commit()
    return jsonify(responses_api.ResponsesAPI.result_true())


@bp.route('/me', methods=('GET',))
def me():
    api_key = request.headers.get('Api-Key')

    if api_key == 'test':
        return jsonify(responses_api.ResponsesAPI.result_true({'user': {'name': 'test'}}))

    db = database.get_db()
    user = db.execute(
        select(
            User,
            Follow.author_id,
            Follow.follower_id
        ).where(
            User.api_key == api_key
        )
    ).scalar()

    if user:
        user_dict = user.to_dict()
        user_dict['followers'] = [f.follower.to_dict(exclude=('api_key',)) for f in user.follows_author]
        user_dict['following'] = [f.author.to_dict(exclude=('api_key',)) for f in user.follows_follower]
        return jsonify(responses_api.ResponsesAPI.result_true({'user': user_dict}))
    return jsonify(responses_api.ResponsesAPI.error_not_found(f'User with api-key {api_key} not found'))


@bp.route('/<int:user_id>', methods=('GET',))
def get_user_by_id(user_id):
    db = database.get_db()

    user = db.execute(
        select(
            User,
            Follow.author_id,
            Follow.follower_id
        ).where(
            User.id == user_id
        )
    ).scalar()

    if user:
        user_dict = user.to_dict()
        user_dict['followers'] = [f.follower.to_dict(exclude=('api_key',)) for f in user.follows_author]
        user_dict['following'] = [f.author.to_dict(exclude=('api_key',)) for f in user.follows_follower]
        return jsonify(responses_api.ResponsesAPI.result_true({'user': user_dict}))
    return jsonify(responses_api.ResponsesAPI.error_not_found(f'User with id {user_id} not found'))
