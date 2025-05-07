# app/config.py stays exactly as before:
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default secret key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        'sqlite:///' + os.path.join(basedir, '..', 'data-dev.sqlite')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'SimpleCache'  # Can be 'RedisCache', 'FileSystemCache', etc.
    CACHE_DEFAULT_TIMEOUT = 300  # Cache timeout in seconds

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///:memory:')

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

config = {
    'development': DevelopmentConfig,
    'testing':    TestingConfig,
    'production': ProductionConfig,
    'default':    DevelopmentConfig
}