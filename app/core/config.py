import os
import sys
from dotenv import load_dotenv

# Load environmental variables from .env file
load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""

    ENV: str = os.getenv("FLASK_ENV", "development")
    DEBUG: bool = ENV == "development"
    PORT: int = int(os.getenv("PORT", 5000))

    # Ensure DATABASE_URL is defined in the environment, except during unit tests
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        if "pytest" in sys.modules:
            # Secure fallback during test execution context
            DATABASE_URL = "postgresql+asyncpg://postgres:dummy@localhost:5432/dummy"
        else:
            raise ValueError(
                "Missing DATABASE_URL environment variable. Please define it in your .env file."
            )

    # Flask-Smorest & Swagger Settings
    API_TITLE: str = "Employee Management API"
    API_VERSION: str = "v1"
    OPENAPI_VERSION: str = "3.0.3"
    OPENAPI_URL_PREFIX: str = "/"
    OPENAPI_SWAGGER_UI_PATH: str = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI: str = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
