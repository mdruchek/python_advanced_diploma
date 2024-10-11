class Config(object):
    """
    Класс конфигурации приложения по умолчанию

    Attributes:
        TESTING (bool): режим тестирования
        ECHO_ENGINE_DATABASE (bool): отображение SQL запросов в консоле при работе приложения
        UPLOAD_FOLDER (str): папка загрузки пользовательских файлов
        ALLOWED_EXTENSIONS (tuple): допустимые расширения пользовательских файлов
    """

    TESTING = False
    ECHO_ENGINE_DATABASE = False
    UPLOAD_FOLDER = 'medias'
    ALLOWED_EXTENSIONS = ('jpg', 'jpeg')


class ProductionConfig(Config):
    """
    Класс конфигурации эксплуатации приложения

    Attributes:
        ENVIRONMENT (str): виртуальное окружение приложения
        DATABASE (str): Настройка подключения к базе данных
    """

    ENVIRONMENT = 'prod'
    DATABASE = 'postgresql+psycopg2://admin:admin@db:5432/twitter_clone_db'


class DevelopmentConfig(Config):
    """
    Класс конфигурации разработки приложения

    Attributes:
        ENVIRONMENT (str): виртуальное окружение приложения
        DATABASE (str): Настройка подключения к базе данных
        ECHO_ENGINE_DATABASE (bool): отображение SQL запросов в консоле при работе приложения
        SECRET_KEY (str): секретный ключ приложения
    """

    ENVIRONMENT = 'dev'
    DATABASE = 'sqlite:///{instance_path}/dev_database.db'
    ECHO_ENGINE_DATABASE = False
    SECRET_KEY = 'dev'


class TestingConfig(Config):
    """
    Класс конфигурации тестирования приложения

    Attributes:
        DATABASE_URI (str): Настройка подключения к базе данных
        ECHO_ENGINE_DATABASE (bool): отображение SQL запросов в консоле при работе приложения
        TESTING (bool): режим тестирования
    """

    DATABASE = 'sqlite:///:memory:'
    TESTING = True
