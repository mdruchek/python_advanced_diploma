class Config(object):
    TESTING = False
    SECRET_KEY = 'dev'


class ProductionConfig(Config):
    DATABASE_URI = ...
    SECRET_KEY = ''


class DevelopmentConfig(Config):
    DATABASE_URI = ...


class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
