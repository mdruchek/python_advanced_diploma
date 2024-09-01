from flask import Blueprint


bp = Blueprint('tweet', __name__, url_prefix='/api/tweets')
