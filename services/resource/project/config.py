# services/resource/project/config.py


import os


# current dirname
basedir = os.path.dirname(__file__)


class BaseConfig:
    """Base configuration."""
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    # Does not use os.getenv or 'get' method, we need the error message
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_DEV_URL']
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True

    # this config is important for testing when something error
    # otherwise you can wrapper you test in 'with self.app.test_client()'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_TEST_URL']
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0
    TOKEN_EXPIRATION_SECONDS = 3


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
