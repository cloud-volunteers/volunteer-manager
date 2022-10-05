from os import getenv

class Config:
    APP_NAME = getenv('APP_NAME')
    APP_ENV = getenv('APP_ENV')
    LOGGING_LEVEL = getenv('LOGGING_LEVEL')
    COLORED_LOGGING = getenv('COLORED_LOGGING')
    DATABASE_URL = getenv('DATABASE_URL')