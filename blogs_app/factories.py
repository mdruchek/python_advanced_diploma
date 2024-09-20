import string

import factory
from factory.fuzzy import FuzzyText

from blogs_app import database
from blogs_app import models


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.User
        sqlalchemy_session = database.get_db()
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('first_name', locale='ru_Ru')
    api_key = FuzzyText(length=5, chars=string.ascii_letters+string.digits)


class TweetFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Tweet
        sqlalchemy_session = database.get_db()
        sqlalchemy_session_persistence = 'commit'

    content = factory.Faker('sentence', nb_words=5, variable_nb_words=True, locale='ru_Ru')
    author_id = factory.Faker('pyint', min_value=1, max_value=5, step=1)


class LikeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Like
        sqlalchemy_session = database.get_db()
        sqlalchemy_session_persistence = 'commit'

    user_id = factory.Faker('pyint', min_value=1, max_value=5, step=1)
    tweet_id = factory.Faker('pyint', min_value=1, max_value=5, step=1)


class MediaFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Media
        sqlalchemy_session = database.get_db()
        sqlalchemy_session_persistence = 'commit'

    tweet_id = factory.Faker('pyint', min_value=1, max_value=5, step=1)
    url = factory.Faker('file_path', extension='jpg')


class FollowFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Follow
        sqlalchemy_session = database.get_db()
        sqlalchemy_session_persistence = 'commit'

    author_id = factory.Faker('pyint', min_value=1, max_value=5, step=1)
    follower_id = factory.Faker('pyint', min_value=1, max_value=5, step=1)
