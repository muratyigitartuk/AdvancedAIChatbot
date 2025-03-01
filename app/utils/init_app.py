"""Application initialization utilities.

This module provides functions to initialize the application database,
create test users, and set up sample data for development purposes.
"""

import os
import yaml
from sqlalchemy.orm import Session
from app.db.models import User, Conversation, Message
from app.db.database import get_db, engine, Base
import datetime


def init_database():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def load_config(config_path):
    """Load YAML configuration file."""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def create_test_user(db: Session):
    """Create a test user for development purposes."""
    # Check if test user already exists
    test_user = db.query(User).filter(User.username == "test_user").first()
    if test_user:
        print("Test user already exists.")
        return test_user

    # Create test user
    test_user = User(
        username="test_user",
        email="test@example.com",
        hashed_password=os.getenv(
            "TEST_USER_PASSWORD",
            "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        ),  # "password"
        full_name="Test User",
        is_active=True,
        preferences={"theme": "dark", "language": "en", "notification_level": "medium"},
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    print(f"Test user created with ID: {test_user.id}")

    # Create a sample conversation
    conversation = Conversation(user_id=test_user.id, title="Welcome Conversation")
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    # Add sample messages
    messages = [
        Message(
            conversation_id=conversation.id,
            content="Hello! How can you help me?",
            is_user=True,
            message_metadata={"sentiment": {"label": "POSITIVE", "score": 0.92}},
        ),
        Message(
            conversation_id=conversation.id,
            content="I'm your AI assistant. I can help you with information, answering questions, setting reminders, and more. What would you like to know?",
            is_user=False,
            message_metadata={},
        ),
        Message(
            conversation_id=conversation.id,
            content="Can you tell me about machine learning?",
            is_user=True,
            message_metadata={"topics": ["technology", "education"]},
        ),
        Message(
            conversation_id=conversation.id,
            content="Machine learning is a subset of artificial intelligence that enables computers to learn from data and improve from experience without being explicitly programmed. It focuses on developing algorithms that can access data and use it to learn patterns.",
            is_user=False,
            message_metadata={},
        ),
    ]

    for message in messages:
        db.add(message)

    db.commit()
    print(f"Sample conversation created with ID: {conversation.id}")

    return test_user


def initialize_app():
    """Initialize the application with required data."""
    # Initialize database
    init_database()

    # Get database session
    db = next(get_db())

    try:
        # Create test user
        create_test_user(db)

        print("Application initialized successfully!")
    except Exception as e:
        print(f"Error initializing application: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    initialize_app()
