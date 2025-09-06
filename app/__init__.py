from flask import Flask
from .database.models import db
from .api.routes import api_bp
from config import Config, DevelopmentConfig

def create_app(config_class: Config = DevelopmentConfig):
    """
    The application factory. Creates and configures an instance of the Flask application,
    making it modular and easy to test.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    app.register_blueprint(api_bp, url_prefix='/api')

    # Ensure the database tables are created within the application context.
    with app.app_context():
        db.create_all()

    return app