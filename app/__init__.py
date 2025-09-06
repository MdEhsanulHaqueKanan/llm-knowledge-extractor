from flask import Flask
from .database.models import db
from .api.routes import api_bp
from config import Config, DevelopmentConfig

def create_app(config_class: Config = DevelopmentConfig):
    """
    The application factory. It creates and configures an instance of the Flask application.
    This pattern makes the application modular and easy to test.
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # Load the configuration from the config object we created earlier.
    app.config.from_object(config_class)

    # Initialize the database with our Flask app.
    db.init_app(app)

    # Register our API blueprint. All routes in this blueprint will be prefixed with /api.
    # For example, '/analyze' becomes '/api/analyze'.
    app.register_blueprint(api_bp, url_prefix='/api')

    # This block ensures that the database tables are created when the app starts.
    # It runs within the 'application context', which has knowledge of the app's configuration.
    with app.app_context():
        db.create_all()

    return app