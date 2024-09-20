from flask import Blueprint, request
from sqlalchemy import select

from blogs_app import database
from blogs_app import models
from blogs_app import schemas


bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/me', methods=('GET',))
def me():
    api_key = request.args.get('api-key')
    db = database.get_db()
    user = db.execute(select(models.User).where(models.User.api_key == api_key))
    return user.mo
    # {
    #     "result": True,
    #     "user": {
    #         "id": 6,
    #         "name": 'Кнопочка',
    #         "followers":[
    #             {
    #                 "id":1,
    #                 "name":"Семён"
    #             }
    #         ],
    #         "following":[
    #             {
    #                 "id":2,
    #                 "name":"Лавр"
    #             }
    #         ]
    #     }
    # }
