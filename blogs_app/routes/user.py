from flask import Blueprint, request, jsonify
from sqlalchemy import select

from blogs_app import database
from blogs_app import models
from blogs_app import schemas


bp = Blueprint('users', __name__, url_prefix='/api/users')

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
        return jsonify(
            {
                'result': True,
                'user': user_dict
            }
        )
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
