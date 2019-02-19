import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    SECRET = os.getenv('SECRET') 
    """gets the secret key set in the .env file"""
    DATABASE_URI = os.getenv('DATABASE_URL')
class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_URL')
    SECRET = os.getenv('SECRET') 

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DATABASE_URL = os.getenv('DATABASE_URL')
    DEBUG = True
    SECRET = os.getenv('SECRET') 

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True
class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}