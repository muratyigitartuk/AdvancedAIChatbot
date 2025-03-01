"""
Database Configuration Module

This module handles the database connection setup for the application.
It configures SQLAlchemy to connect to a PostgreSQL database using
environment variables for configuration.

The module provides:
- Database connection configuration
- SQLAlchemy engine and session setup
- Base class for declarative models
- Dependency function for FastAPI to get database sessions
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "chatbot_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

# Construct database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that provides a database session.

    This function creates a new SQLAlchemy session for each request,
    and ensures that the session is closed after the request is completed,
    even if an exception occurs during the request.

    Yields:
        Session: SQLAlchemy database session

    Example:
        ```python
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items
        ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
