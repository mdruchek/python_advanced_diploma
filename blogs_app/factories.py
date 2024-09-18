import string

import factory
from factory.fuzzy import FuzzyText

from .models import User
from .database import get_db


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = get_db()
        sqlalchemy_get_or_create = ('api_key',)

    name = factory.Faker('first_name', locale='ru_Ru')
    api_key = FuzzyText(length=5, chars=string.ascii_letters+string.digits)
