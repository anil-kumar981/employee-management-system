from flask import Flask
from app.core.config import Config
from app.database.database import init_db
from app.database.migration_runner import run_migrations
from app.shared.error_handlers import register_error_handlers
from app.controllers.employee_controller import employee_bp
from app.shared.swagger import swagger_bp
from app.middleware.logging_middleware import APILoggingMiddleware


def create_app() -> Flask:
    """Application factory that configures and instantiates the Flask API.

    Performs standard bootstraps:
    - Loads configuration schemas.
    - Binds and auto-initializes the database engine and tables.
    - Hooks global custom exception routers.
    - Registers routing Blueprints (employees & dynamic Swagger docs).
    """
    app = Flask(__name__)

    # Load configuration parameters
    app.config.from_object(Config)

    # Silently apply any pending migrations before DB connections are opened
    run_migrations()

    # Initialize DB connection and create database schemas
    init_db(app)

    # Register centralized exception formatting handlers
    register_error_handlers(app)

    # Register logging middleware
    APILoggingMiddleware(app)

    # Register standard Flask routing blueprints
    app.register_blueprint(employee_bp)
    app.register_blueprint(swagger_bp)

    return app
