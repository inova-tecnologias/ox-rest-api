import os
from dotenv import load_dotenv


load_dotenv()

class Config(object):
    """
    Common configurations
    """
    
    SECRET_KEY = os.getenv('OXAPI_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('OXAPI_DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV=os.getenv('OXAPI_ENVIRONMENT', default='development')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = False
    USE_OX = os.getenv('OXAPI_USEOXCLOUD', default=False)


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    SQLALCHEMY_ECHO = False
    USE_OX = os.getenv('OXAPI_USEOXCLOUD', default=True)

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

app_config = app_config[os.getenv('OXAPI_ENVIRONMENT', default='development')]