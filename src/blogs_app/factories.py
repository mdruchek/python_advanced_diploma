import string

import factory
from factory.fuzzy import FuzzyText

from .database import get_session
from blogs_app import models


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Фабрика для тестового заполнения модели User

    Attributes:
        name (str): Имя пользователя
        api_key (str): api_key пользователя
    """

    class Meta:
        model = models.User
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('first_name', locale='ru_Ru')
    api_key = FuzzyText(length=5, chars=string.ascii_letters+string.digits)


class TweetFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Фабрика для тестового заполнения модели твита

    Attributes:
        content (str): содержание твита
        author_id (int): id автора твита
    """

    class Meta:
        model = models.Tweet
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = 'commit'

    content = factory.Faker('sentence', nb_words=5, variable_nb_words=True, locale='ru_Ru')
    author_id = factory.Faker('pyint', min_value=1, max_value=5, step=1)
