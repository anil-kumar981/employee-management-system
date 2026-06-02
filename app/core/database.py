from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models, utilizing modern SQLAlchemy 2.0 DeclarativeBase."""
    pass

# Shared SQLAlchemy instance
db = SQLAlchemy(model_class=Base)

def init_db(app):
    """Initialize the database with the Flask app context and create all tables."""
    db.init_app(app)
    
    with app.app_context():
        # Enable Foreign Keys for SQLite if utilized
        if "sqlite" in app.config.get("SQLALCHEMY_DATABASE_URI", ""):
            from sqlalchemy import event
            @event.listens_for(db.engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
                
        db.create_all()

