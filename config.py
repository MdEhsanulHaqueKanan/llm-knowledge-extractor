import os
from dotenv import load_dotenv

# This function loads the variables from your .env file into the environment
load_dotenv()

class Config:
    """Base configuration class. Contains default settings."""
    # A secret key is needed for session management and other security features in Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a-very-secret-key')
    # This disables a Flask-SQLAlchemy feature that we don't need and adds overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Configuration for local development."""
    # Specifies the database file for development. It will be created in an 'instance' folder.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

class TestingConfig(Config):
    """Configuration for running automated tests."""
    TESTING = True
    # For tests, we use an in-memory SQLite database.
    # This is faster and ensures that tests are isolated and don't leave behind files.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'