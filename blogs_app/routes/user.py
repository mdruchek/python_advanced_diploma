from flask import Blueprint, request
from sqlalchemy import select

from blogs_app import database
from blogs_app import models
from blogs_app import schemas


bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/me', methods=('GET',))
def me():
    api_key = request.headers.get('Api-Key')
    db = database.get_db()
    user = db.execute(select(models.User).where(models.User.api_key == api_key)).scalar()
    # user_dict = user.to_dict()
    # user = schemas.UserSchema(**user_dict)
    return {#user.model_dump_json()
        "result": True,
        "user": {
            "id": 6,
            "name": 'Кнопочка',
            "followers":[
                {
                    "id":1,
                    "name":"Семён"
                }
            ],
            "following":[
                {
                    "id":2,
                    "name":"Лавр"
                }
            ]
        }
    }
