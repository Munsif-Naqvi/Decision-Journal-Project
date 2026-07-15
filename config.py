# CONFIGURES

# os lets us access the environment variables
import os
from datetime import timedelta

from dotenv import load_dotenv
# and load_dotenv() reads the '.env' file and actually loads its value in the environment
# without load_dotenv(), os won't be able to find variables in '.env'

load_dotenv() # call and load the variables

# the base Config class with the required secrets
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') # gets the defined SECRET_KEY from '.env'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

# inherits the base Config class, and overrides the changes it wants
class DevelopmentConfig(Config):
    DEBUG = True

# inherits the base Config class, and overrides the changes it wants
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"

# inherits the base Config class, and overrides the changes it wants
class ProductionConfig(Config):
    DEBUG = False

# create a dictionary to avoid adding a bunch of if statements in create_app(),
# would only need to pass a name like, (development or testing)
# to define the environment and to keep config. aligned.
# And also, it'd be easier to add more environments lie (staging) later on
config_by_name = {
    'development': DevelopmentConfig, #this is the class which will be stored in key (development)
    'testing': TestingConfig,
    'production': ProductionConfig,
}