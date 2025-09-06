import pytest
from app import create_app
from app.database.models import db
from config import TestingConfig

@pytest.fixture(scope='module')
def test_app():
    """Creates and configures a new app instance for each test module."""
    app = create_app(TestingConfig)
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def test_client(test_app):
    """Creates a test client to make virtual requests to the app."""
    return test_app.test_client()

@pytest.fixture(scope='function')
def init_database(test_app):
    """
    Sets up a clean, in-memory database for each test function.
    'scope=function' ensures that tests are isolated and don't share state.
    """
    db.create_all()
    yield db
    db.drop_all()