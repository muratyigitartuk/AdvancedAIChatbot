"""
Database Models Module

This module defines the SQLAlchemy ORM models that represent the database schema
for the Advanced AI Chatbot application. It includes models for users, conversations,
messages, and user topics.

The models define the structure of the database tables and their relationships:
- Users have many conversations
- Conversations belong to a user and have many messages
- Messages belong to a conversation
- User topics track topics of interest for each user
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()


class User(Base):
    """
    User model representing application users.

    This model stores user authentication information, profile details,
    and preferences. It has a one-to-many relationship with conversations.

    Attributes:
        id (int): Primary key
        username (str): Unique username for login
        email (str): Unique email address
        hashed_password (str): Securely hashed password
        full_name (str): User's full name (optional)
        is_active (bool): Whether the user account is active
        created_at (datetime): When the user account was created
        preferences (JSON): User preferences stored as JSON
        conversations (relationship): List of user's conversations
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    preferences = Column(JSON, default={})

    conversations = relationship("Conversation", back_populates="user")


class Conversation(Base):
    """
    Conversation model representing chat sessions.

    Each conversation belongs to a user and contains multiple messages.
    Conversations are used to group related messages together and provide
    context for the AI responses.

    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to the user who owns this conversation
        title (str): Optional title for the conversation
        created_at (datetime): When the conversation was created
        updated_at (datetime): When the conversation was last updated
        user (relationship): The user who owns this conversation
        messages (relationship): List of messages in this conversation
    """

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    """
    Message model representing individual chat messages.

    Each message belongs to a conversation and can be either from the user
    or from the AI assistant. Messages include content and metadata about
    the message processing.

    Attributes:
        id (int): Primary key
        conversation_id (int): Foreign key to the conversation this message belongs to
        content (str): The text content of the message
        is_user (bool): Whether the message is from the user (True) or AI (False)
        created_at (datetime): When the message was created
        message_metadata (JSON): Additional data about the message (sentiment, entities, etc.)
        conversation (relationship): The conversation this message belongs to
    """

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    content = Column(String)
    is_user = Column(Boolean)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    message_metadata = Column(JSON, default={})

    conversation = relationship("Conversation", back_populates="messages")


class UserTopic(Base):
    """
    UserTopic model tracking topics of interest for users.

    This model stores information about topics that the user has discussed
    or shown interest in. It includes a weight to indicate the level of interest
    and tracks when the topic was last mentioned.

    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to the user
        topic (str): The name of the topic
        weight (int): The importance/relevance of this topic to the user
        last_mentioned (datetime): When the topic was last discussed
    """

    __tablename__ = "user_topics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic = Column(String, index=True)
    weight = Column(Integer, default=1)
    last_mentioned = Column(DateTime, default=datetime.datetime.utcnow)
