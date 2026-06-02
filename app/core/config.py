import os
from dotenv import load_dotenv

# Load environmental variables from .env file
load_dotenv()

class Config:
    """Application configuration loaded from environment variables."""
    ENV: str = os.getenv("FLASK_ENV", "development")
    DEBUG: bool = ENV == "development"
    PORT: int = int(os.getenv("PORT", 5000))
    
    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///employee_management.db")
    
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
