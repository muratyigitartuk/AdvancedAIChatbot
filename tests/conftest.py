"""
Test Configuration Module

This module provides test fixtures and configurations for the advanced AI chatbot
application. It sets up an in-memory SQLite database for testing purposes and
provides fixtures for:

1. Database session - Creates and manages test database sessions
2. Test client - Configures a FastAPI TestClient with database overrides
3. Test user - Creates a sample user for authentication tests
4. Test user token - Generates a valid JWT token for the test user
5. Test conversation - Creates a sample conversation with messages for chat tests

These fixtures allow tests to be executed in isolation with controlled test data,
without affecting any production database. Each test function can request
these fixtures as parameters to set up the necessary test environment.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db
from app.db.models import User, Conversation, Message
from app.core.auth import AuthConfig


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Create a database session for testing."""
    # Create the database tables
    Base.metadata.create_all(bind=engine)

    # Create a session for testing
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

    # Drop the tables after the test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Create a FastAPI test client with database overrides."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Create a test user for authentication testing."""
    # Create a test user
    hashed_password = AuthConfig.get_password_hash("password123")
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hashed_password,
        full_name="Test User",
        is_active=True,
        preferences={"theme": "dark"},
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def test_user_token(test_user):
    """Generate a valid JWT token for the test user."""
    access_token = AuthConfig.create_access_token(data={"sub": str(test_user.id)})
    return access_token


@pytest.fixture
def test_conversation(db_session, test_user):
    """Create a test conversation with messages for chat testing."""
    # Create a test conversation
    conversation = Conversation(user_id=test_user.id, title="Test Conversation")
    db_session.add(conversation)
    db_session.commit()
    db_session.refresh(conversation)

    # Add user message
    user_message = Message(
        conversation_id=conversation.id,
        content="Hello, AI assistant!",
        is_user=True,
        message_metadata={"sentiment": {"label": "POSITIVE", "score": 0.9}},
    )
    db_session.add(user_message)

    # Add bot message
    bot_message = Message(
        conversation_id=conversation.id,
        content="Hello! How can I help you today?",
        is_user=False,
        message_metadata={"generated_from": "test-model"},
    )
    db_session.add(bot_message)

    db_session.commit()

    return conversation
