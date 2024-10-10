import json
import os
from collections.abc import Sequence
from typing import Optional

from flask import Blueprint, request, jsonify, url_for, current_app, Response
from sqlalchemy import select, delete, ScalarResult
from sqlalchemy.orm import Session

from blogs_app import database
from blogs_app.models import User, Tweet, Media, Like, Follow
from blogs_app import responses_api


bp = Blueprint('tweet', __name__, url_prefix='/api/tweets')


@bp.route('/', methods=('POST',))
def create_tweet() -> tuple[Response, Optional[int]]:
    """
    Эндпоинт создания твита

    :return: Ответ удачного или не удачного создания твита
    :rtype: Response
    """

    db: Session = database.get_db()
    api_key: str = request.headers.get('Api-Key')
    request_data: Optional[dict] = request.json
    user: Optional[User] = db.execute(select(User).where(User.api_key == api_key)).scalar()

    if not user:
        return jsonify(responses_api.ResponsesAPI.error_not_found(f'User with api-key {api_key} not found')), 404

    tweet: Tweet = Tweet(
        content=request_data['tweet_data'],
        media_ids=json.dumps(request_data.pop('tweet_media_ids'))
    )

    user.tweets.append(tweet)
    db.commit()
    return jsonify(responses_api.ResponsesAPI.result_true({'tweet_id': tweet.id})), 200


@bp.route('/<int:tweet_id>', methods=('DELETE',))
def delete_tweet(tweet_id: int) -> tuple[Response, int]:
    """
    Эндпоинт удаления твита

    :param tweet_id: id твита
    :type tweet_id: int

    :return: Ответ удачного или не удачного удаления твита
    :rtype: Response
    """

    db: Session = database.get_db()
    api_key: str = request.headers.get('Api-Key')
    user: Optional[User] = db.execute(select(User).where(User.api_key == api_key)).scalar()

    if not user:
        return jsonify(responses_api.ResponsesAPI.error_not_found(f"User with api_key {api_key} not found")), 404

    tweet_for_deleted: Optional[Tweet] = db.get(Tweet, tweet_id)

    if not tweet_for_deleted:
        return jsonify(responses_api.ResponsesAPI.error_not_found(f"Tweet with id={tweet_id} not found")), 404

    if not user.id == tweet_for_deleted.author_id:
        return jsonify(responses_api.ResponsesAPI.error_forbidden('User can only delete their own blogs')), 403

    if tweet_for_deleted.media_ids:
        media_ids: list[int] = json.loads(tweet_for_deleted.media_ids)

        url_medias_for_delete: Sequence[str] = db.execute(
            select(Media.url)
            .where(Media.id.in_(media_ids))
        ).scalars().all()

        for url in url_medias_for_delete:
            path_file_for_delete: str = os.path.join(current_app.instance_path, url)

            try:
                os.remove(path_file_for_delete)
            except FileNotFoundError:
                pass

        db.execute(delete(Media).where(Media.id.in_(media_ids)))

    db.delete(tweet_for_deleted)
    db.commit()
    return jsonify(responses_api.ResponsesAPI.result_true()), 200


@bp.route('/<int:tweet_id>/likes', methods=('POST',))
def create_like_on_tweet(tweet_id: int) -> tuple[Response, int]:
    """
    Эндпоинт добавления лайка на твит

    :param tweet_id: id твита
    :type tweet_id: int

    :return: Ответ удачного или не удачного добавлния лайка на твит
    :rtype: Response
    """

    db: Session = database.get_db()
    api_key: str = request.headers.get('Api-Key')
    user: Optional[User] = db.execute(select(User).where(User.api_key == api_key)).scalar()

    if not user:
        return jsonify(responses_api.ResponsesAPI.error_not_found(f"User with api_key {api_key} not found")), 404

    tweet_for_like: Optional[Tweet] = db.get(Tweet, tweet_id)

    if not tweet_for_like:
        return jsonify(responses_api.ResponsesAPI.error_not_found(f"Tweet with id={tweet_id} not found")), 404

    if not user.id == tweet_for_like.author_id:
        like: Like = Like(user_id=user.id)
        tweet_for_like.likes.append(like)
        db.commit()
        return jsonify(responses_api.ResponsesAPI.result_true()), 200

    return jsonify(responses_api.ResponsesAPI.error_forbidden("You can only like other people's blogs")), 403


@bp.route('/<int:tweet_id>/likes', methods=('DELETE',))
def delete_like_with_blog(tweet_id):
    """
    Эндпоинт удаления лайка с твита

    :param tweet_id: id твита
    :type tweet_id: int

    :return: Ответ удачного или не удачного удаления лайка с твита
    :rtype: Response
    """

    db: Session = database.get_db()
    api_key: str = request.headers.get('Api-Key')
    user: Optional[User] = db.execute(select(User).where(User.api_key == api_key)).scalar()

    if not user:
        return jsonify(responses_api.ResponsesAPI.error_not_found(f"User with api_key {api_key} not found")), 404

    db.execute(
        delete(Like)
        .where(Like.user_id == user.id)
        .where(Like.tweet_id == tweet_id)
    )

    db.commit()
    return jsonify(responses_api.ResponsesAPI.result_true())


@bp.route('/', methods=('GET',))
def get_tweets():
    """
    Эндпоинт список твитов

    :return: Ответ со списком всех твитов
    :rtype: Response
    """

    db: Session = database.get_db()
    tweets: Sequence[Tweet] = db.execute(select(Tweet).order_by(Tweet.id.desc())).scalars().all()
    tweets_list_of_dict = []

    for tweet in tweets:
        tweet_dict: dict = tweet.to_dict()
        tweet_dict.pop('author_id')
        tweet_dict['author']: dict = tweet.author.to_dict(exclude=('api_key',))
        tweet_dict['likes']: list = [like.user.to_dict(exclude=('api_key',)) for like in tweet.likes]
        media_ids_json: str = tweet_dict.pop('media_ids')

        if media_ids_json:
            media_ids_list: list = json.loads(media_ids_json)

            media_links: Sequence[str] = (
                db.execute(select(Media.url).where(Media.id.in_(media_ids_list)))
                .scalars()
                .all()
            )

            tweet_dict['attachments']: str = [
                url_for('download_file', relative_link=link.replace('\\', '/'))
                for link in media_links
            ]

        for like_dict in tweet_dict['likes']:
            like_dict['user_id'] = like_dict.pop('id')

        tweets_list_of_dict.append(tweet_dict)

    return jsonify(responses_api.ResponsesAPI.result_true({'tweets': tweets_list_of_dict})) 
