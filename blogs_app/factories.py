import string

import factory
from factory.fuzzy import FuzzyText

from .models import User
from blogs_app import database

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = database.Session()
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker('first_name', locale='ru_Ru')
    api_key = FuzzyText(length=5, chars=string.ascii_letters+string.digits)
