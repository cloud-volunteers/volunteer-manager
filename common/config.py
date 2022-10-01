from dotenv import dotenv_values
from os import getenv

config = dotenv_values(".env")

class Config:
    APP_NAME = getenv('APP_NAME') or config.get('APP_NAME')
    APP_ENV = getenv('APP_ENV') or config.get('APP_ENV')
    LOGGING_LEVEL = getenv('LOGGING_LEVEL') or config.get('LOGGING_LEVEL')
    COLORED_LOGGING = getenv('COLORED_LOGGING') or config.get('COLORED_LOGGING')

    if APP_ENV == 'DOCKER':
        DATABASE_URL = getenv('DATABASE_URL')