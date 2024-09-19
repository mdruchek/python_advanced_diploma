class Config(object):
    TESTING = False
    ECHO_ENGINE_DATABASE = False


class ProductionConfig(Config):
    ENVIRONMENT = 'prod'
    DATABASE = 'postgresql+psycopg2://admin:admin@db:5432/twitter_clone_db'


class DevelopmentConfig(Config):
    ENVIRONMENT = 'dev'
    DATABASE = 'sqlite:///{instance_path}/dev_database.db'
    ECHO_ENGINE_DATABASE = True
    SECRET_KEY = 'dev'


class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
