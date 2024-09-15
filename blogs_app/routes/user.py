from flask import Blueprint, request


bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/me', methods=('GET',))
def me():
    api_kyi = request.args.get('api-key')
    return {
        "result": True,
        "user": {
            "id": 1,
            "name": 'Незнайка',
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
    }
