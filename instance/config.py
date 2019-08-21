import os

class Config(object):
    """Parent configuration class."""
    DEBUG = True

class Development(Config):
    """Configurations for Development."""
    DEBUG = True
    DB_URL = "dbname='store_manager' host='localhost' port='5432' user='postgres' password='Password2#'"

class Testing(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True
    DB_URL = "dbname='store_manager_test' host='localhost' port='5432' user='postgres' password='Password2#'"

class Staging(Config):
    """Configurations for Staging."""
    DEBUG = True

class Production(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    DB_URL = "postgres://qvlmvjritnsqtg:f7d77803ffd16c21c1ee2a2d63e47108aab0a5b21b43d7bf2a7cd9c24a5d6746@ec2-54-83-49-109.compute-1.amazonaws.com:5432/d8cvs0ipt09ua3"

config = {
    'development': Development,
    'testing': Testing,
    'staging': Staging,
    'production': Production
}
