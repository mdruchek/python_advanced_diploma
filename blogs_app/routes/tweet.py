import json

from flask import Blueprint, request, jsonify
from sqlalchemy import select

from blogs_app import database
from blogs_app import models
from blogs_app import responses_api
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
    return jsonify(responses_api.ResponsesAPI.result_true({'tweet_id': tweet.id}))


@bp.route('/<int:tweet_id>', methods=('DELETE',))
def delete_tweet(tweet_id):
    db = database.get_db()
    api_key = request.headers.get('Api-Key')
    user = db.execute(select(models.User).where(models.User.api_key == api_key)).scalar()
    tweet_for_deleted = db.get(models.Tweet, tweet_id)
    if not tweet_for_deleted:
        return jsonify(responses_api.ResponsesAPI.error_not_found(f"Tweet with id={tweet_id} not found")), 404
    if user.id == tweet_for_deleted.author_id:
        db.delete(tweet_for_deleted)
        db.commit()
        return jsonify(responses_api.ResponsesAPI.result_true())
    return jsonify(responses_api.ResponsesAPI.error_forbidden('User can only delete their own blogs')), 403


@bp.route('/<int:tweet_id>/likes', methods=('POST',))
def create_like_on_blog(tweet_id):
    db = database.get_db()
    api_key = request.headers.get('Api-Key')
    user = db.execute(select(models.User).where(models.User.api_key == api_key)).scalar()
    tweet_for_like = db.get(models.Tweet, tweet_id)
    if not tweet_for_like:
        return jsonify(responses_api.ResponsesAPI.error_not_found(f"Tweet with id={tweet_id} not found")), 404
    if not user.id == tweet_for_like.author_id:
        like = models.Like(user_id=user.id)
        tweet_for_like.likes.append(like)
        db.commit()
        return jsonify(responses_api.ResponsesAPI.result_true())
    return jsonify(responses_api.ResponsesAPI.error_forbidden("You can only like other people's blogs")), 403


@bp.route('/<int:id_tweet>/likes', methods=('DELETE',))
def delete_like_with_blog(id_tweet):
    db = database.get_db()
    api_key = request.headers.get('Api-Key')
    user = db.execute(select(models.User).where(models.User.api_key == api_key)).scalar()

    like = db.execute(
        select(models.Like)
        .where(models.Like.user_id == user.id and models.Like.tweet_id == id_tweet)
    ).scalar()
    
    db.delete(like)
    db.commit()
    return jsonify(responses_api.ResponsesAPI.result_true())


@bp.route('/', methods=('GET',))
def get_tweets():
    db = database.get_db()
    tweets = db.execute(select(models.Tweet).order_by(models.Tweet.id.desc())).scalars().all()
    tweets_list_of_dict = []
    for tweet in tweets:
        tweet_dict = tweet.to_dict()
        tweet_dict.pop('author_id')
        tweet_dict['author'] = tweet.author.to_dict(exclude=('api_key',))
        tweet_dict['likes'] = [like.user.to_dict(exclude=('api_key',)) for like in tweet.likes]
        # tweet_dict['attachments'] = tweet_dict.pop('media_ids')
        tweet_dict.pop('media_ids')
        for like_dict in tweet_dict['likes']:
            like_dict['user_id'] = like_dict.pop('id')
        tweets_list_of_dict.append(tweet_dict)
    print(tweets_list_of_dict)
    print(responses_api.ResponsesAPI.result_true())
    return jsonify(responses_api.ResponsesAPI.result_true({'tweets': tweets_list_of_dict}))
