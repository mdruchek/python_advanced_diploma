from flask import Blueprint, request, jsonify
from sqlalchemy import select

from blogs_app import database
from blogs_app import models
from blogs_app import responses_api
from blogs_app import schemas
from blogs_app.responses_api import ResponsesAPI

bp = Blueprint('users', __name__, url_prefix='/api/users')


@bp.route('/<int:author_id>/follow', methods=('POST',))
def create_follow(author_id):
    db = database.get_db()
    api_key = request.headers.get('Api-Key')
    user = db.execute(select(models.User).where(models.User.api_key == api_key)).scalar()
    author = db.get(models.User, author_id)
    if not author:
        return jsonify(
            responses_api.ResponsesAPI.error(
                type='Not found',
                message=f"Author with id={author_id} not found"
            )
        ), 404

    if user.id == author.id:
        return jsonify(
            responses_api.ResponsesAPI.error(
                type='Forbidden',
                message="The user cannot follow himself"
            )
        ), 403

    follow_for_create = models.Follow(author_id=author_id, follower=user.id)
    db.add(follow_for_create)
    db.commit()
    return jsonify(responses_api.ResponsesAPI.result_true())


@bp.route('/<int:author_id>/follow', methods=('DELETE',))
def delete_follow(author_id):
    db = database.get_db()
    api_key = request.headers.get('Api-Key')
    user = db.execute(select(models.User).where(models.User.api_key == api_key)).scalar()
    author = db.get(models.User, author_id)
    if not author:
        return jsonify(responses_api.ResponsesAPI.error_not_found(f"Author with id={author_id} not found")), 404
    if user.id == author.id:
        return jsonify(responses_api.ResponsesAPI.error_forbidden("The user cannot unfollow himself")), 403

    follow_for_delete = db.execute(
        select(
            models.Follow
        )
        .where(
            models.Follow.follower_id == user.id
            and models.Follow.author_id == author.id
        )
    ).scalar()

    db.delete(follow_for_delete)
    db.commit()
    return jsonify(responses_api.ResponsesAPI.result_true())


@bp.route('/me', methods=('GET',))
def me():
    api_key = request.headers.get('Api-Key')
    db = database.get_db()
    user = db.execute(
        select(
            models.User,
            models.Follow.author_id,
            models.Follow.follower_id
        ).where(
            models.User.api_key == api_key
        )
    ).scalar()

    if user:
        user_dict = user.to_dict()
        user_dict['followers'] = [f.follower.to_dict(exclude=('api_key',)) for f in user.follows_author]
        user_dict['following'] = [f.author.to_dict(exclude=('api_key',)) for f in user.follows_follower]
        return jsonify(responses_api.ResponsesAPI.result_true({'user': user_dict}))
    return jsonify(
        # {
        #     'result': False,
        #     'error_type': 'str',
        #     'error_message': 'str'
        # }
    # )
    {
        'result' : True,
        "user": {
        "id":"int",
        "name":"str",
        "followers":[
            {
                "id":"int",
                "name":"str"
            }
        ],
        "following":[
            {
                "id":"int",
                "name":"str"
            }
        ]
        }
    })
