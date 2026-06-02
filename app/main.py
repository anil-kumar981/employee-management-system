from flask import Flask
from flask_smorest import Api
from app.core.config import Config
from app.core.database import init_db
from app.core.error_handlers import register_error_handlers
from app.controllers.employee_controller import blp as employee_blueprint

def create_app() -> Flask:
    """Application factory that configures and instantiates the core Flask API.
    
    Performs standard bootstraps:
    - Loads configuration schemas.
    - Binds and auto-initializes the database engine and tables.
    - Hooks global custom exception routers.
    - Registers Smorest OpenAPI blueprints.
    """
    app = Flask(__name__)
    
    # Load configuration parameters
    app.config.from_object(Config)
    
    # Initialize DB connection and create database schemas
    init_db(app)
    
    # Mount Flask-Smorest API instance
    api = Api(app)
    
    # Register centralized exception formatting handlers (runs after Api to override default Smorest handlers)
    register_error_handlers(app)
    
    # Bind Employee controllers
    api.register_blueprint(employee_blueprint)

    
    return app
