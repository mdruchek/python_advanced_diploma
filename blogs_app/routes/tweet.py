from flask import Blueprint, request, jsonify

from sqlalchemy import select

from blogs_app import database
from blogs_app import models
from blogs_app import schemas


bp = Blueprint('tweet', __name__, url_prefix='/api/tweets')


@bp.route('/', methods=('POST',))
def create_tweet():
    api_key = request.headers.get('Api-Key')
    request_data = request.json
    print(request_data)
    return ''


@bp.route('/', methods=('GET',))
def get_tweets():
    db = database.get_db()
    tweets = db.execute(select(models.Tweet)).scalars().all()
    tweets_list_of_dict = []
    for tweet in tweets:
        tweet_dict = tweet.to_dict()
        tweet_dict.pop('author_id')
        tweet_dict['author'] = tweet.author.to_dict(exclude=('api_key',))
        tweet_dict['likes'] = [like.user.to_dict(exclude=('api_key',)) for like in tweet.likes]
        tweets_list_of_dict.append(tweet_dict)
    print(tweets_list_of_dict)
    return jsonify(
        {
            'result': True,
            'tweets': tweets_list_of_dict
        }
    )


    # {
    # “result”: true,
    # "tweets": [
    #     {
    #         "id": int,
    #         "content": string,
    #         "attachments"[
    #             link_1, // relative?
    # link_2,
    # ...
    # ]
    # "author": {
    #     "id": int
    #     "name": string
    # }
    # “likes”: [
    #     {
    # “user_id”: int,
    # “name”: string
    # }
    # ]
    # },
    # ...,
    # ]
    # }
