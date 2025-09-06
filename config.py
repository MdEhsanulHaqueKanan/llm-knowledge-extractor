import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration for the application."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a-very-secret-key')
    # Disables a Flask-SQLAlchemy feature that adds unnecessary overhead.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Configuration for the local development environment."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

class TestingConfig(Config):
    """Configuration for running automated tests."""
    TESTING = True
    # Use in-memory SQLite for tests to ensure a clean and fast environment.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'