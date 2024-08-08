class Config(object):
    TESTING = False
    SECRET_KEY = 'dev'


class ProductionConfig(Config):
    DATABASE_URI = 'postgresql+psycopg2://admin:admin@db:5432/twitter_clone_db'


class DevelopmentConfig(Config):
    DATABASE_URI = ...


class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
