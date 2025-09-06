import pytest
from app import create_app
from app.database.models import db
from config import TestingConfig

@pytest.fixture(scope='module')
def test_app():
    """
    A Pytest fixture that creates and configures a new app instance for testing.
    'scope=module' means this fixture will be set up once per test module (file).
    """
    # Create the app using our special TestingConfig
    app = create_app(TestingConfig)
    
    # The 'application context' is needed for the app to work correctly.
    with app.app_context():
        yield app # 'yield' passes the app object to the test function

@pytest.fixture(scope='module')
def test_client(test_app):
    """
    A fixture that creates a test client. The client is used to make
    virtual requests to our app's endpoints (e.g., POST /api/analyze) without
    needing to run a live server.
    """
    return test_app.test_client()

@pytest.fixture(scope='function')
def init_database(test_app):
    """
    A fixture to set up a clean in-memory database for each test function.
    'scope=function' means this will run before and after every single test.
    This guarantees that our tests are isolated and don't interfere with each other.
    """
    # Create all the tables in our in-memory SQLite database
    db.create_all()

    yield db # The test runs at this point

    # After the test is finished, drop all tables to leave it clean for the next test.
    db.drop_all()