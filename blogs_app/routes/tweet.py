from flask import Blueprint, request

from blogs_app import schemas


bp = Blueprint('tweet', __name__, url_prefix='/api/tweets')


@bp.route('/', methods=('POST',))
def create_tweet():
    api_key = request.headers.get('Api-Key')
    request_data = request.json
    print(request_data)
    return ''
