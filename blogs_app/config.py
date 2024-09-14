class Config(object):
    TESTING = False


class ProductionConfig(Config):
    DATABASE_URI = 'postgresql+psycopg2://admin:admin@db:5432/twitter_clone_db'


class DevelopmentConfig(Config):
    DATABASE_URI = 'sqlite:///tmp/develop_database.db'
    SECRET_KEY = 'dev'


class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
