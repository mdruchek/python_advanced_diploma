import json

from flask import Blueprint, request, jsonify
from sqlalchemy import select

from blogs_app import database
from blogs_app import models
from blogs_app import schemas


bp = Blueprint('tweet', __name__, url_prefix='/api/tweets')


@bp.route('/', methods=('POST',))
def create_tweet():
    db = database.get_db()
    api_key = request.headers.get('Api-Key')
    request_data = request.json
    user = db.execute(select(models.User).where(models.User.api_key == api_key)).scalar()
    tweet = models.Tweet(
        content=request_data['tweet_data'],
        media_ids=json.dumps(request_data.pop('tweet_media_ids'))
    )
    user.tweets.append(tweet)
    db.commit()
    return jsonify(
        {
            'result': True,
            'tweet_id': tweet.id,
        }
    )


@bp.route('/<int:id_tweet>', methods=('DELETE',))
def delete_tweet(id_tweet):
    db = database.get_db()
    api_key = request.headers.get('Api-Key')
    user = db.execute(select(models.User).where(models.User.api_key == api_key)).scalar()
    tweet_for_deleted = db.get(models.Tweet, id_tweet)
    if user.id == tweet_for_deleted.author_id:
        db.delete(tweet_for_deleted)
        db.commit()
        return jsonify(
            {
                'result': True
            }
        )
    return jsonify(
        {
            'result': False,
            'error_type': 'Forbidden',
            'error_massage': 'User can only delete their own blogs',
        }
    ), 403



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
        for like_dict in tweet_dict['likes']:
            like_dict['user_id'] = like_dict.pop('id')
        tweets_list_of_dict.append(tweet_dict)
    return jsonify(
        {
            'result': True,
            'tweets': tweets_list_of_dict
        }
    )
