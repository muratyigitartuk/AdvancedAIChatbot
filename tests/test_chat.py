"""
Chat Functionality Tests Module

This module contains tests for the chat functionality of the advanced AI chatbot application.
It tests various chat-related features including:

1. Chat Endpoint
   - Processing new messages with mocked AI responses
   - Handling messages in existing conversations
   - Validating response formats and metadata

2. Conversation History
   - Retrieving user conversation history
   - Verifying conversation structure and message content

3. Proactive Recommendations
   - Generating AI-powered recommendations based on user context
   - Validating recommendation format and content

These tests use mocked AI engine responses to ensure consistent and predictable test results,
while validating that the API endpoints correctly process and return chat-related data.
"""

import pytest
from fastapi import status
from unittest.mock import patch, MagicMock
from app.core.ai_engine import AIEngine

@patch("app.api.chat.AIEngine")
def test_chat_endpoint(mock_ai_engine, client, test_user, test_user_token):
    """Test chat endpoint with mocked AI engine"""
    # Configure the mock to return a predefined response
    mock_instance = MagicMock()
    mock_instance.process_input.return_value = {
        "response": "This is a test response from the AI",
        "metadata": {
            "sentiment": {"label": "NEUTRAL", "score": 0.8},
            "topics": ["test"]
        },
        "proactive_recommendation": "Would you like to know more about testing?"
    }
    mock_ai_engine.return_value = mock_instance
    
    # Test the chat endpoint
    response = client.post(
        "/api/chat",
        json={
            "user_id": test_user.id,
            "message": "Hello, this is a test message",
            "conversation_id": None  # New conversation
        },
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["response"] == "This is a test response from the AI"
    assert "metadata" in data
    assert data["proactive_recommendation"] == "Would you like to know more about testing?"
    assert "conversation_id" in data

@patch("app.api.chat.AIEngine")
def test_chat_with_existing_conversation(mock_ai_engine, client, test_user, test_user_token, test_conversation):
    """Test chat endpoint with an existing conversation"""
    # Configure the mock
    mock_instance = MagicMock()
    mock_instance.process_input.return_value = {
        "response": "Follow-up response",
        "metadata": {"sentiment": {"label": "NEUTRAL", "score": 0.8}},
        "proactive_recommendation": None
    }
    mock_ai_engine.return_value = mock_instance
    
    # Test the chat endpoint with existing conversation
    response = client.post(
        "/api/chat",
        json={
            "user_id": test_user.id,
            "message": "This is a follow-up message",
            "conversation_id": test_conversation.id
        },
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["response"] == "Follow-up response"
    assert data["conversation_id"] == test_conversation.id

def test_get_user_history(client, test_user, test_user_token, test_conversation):
    """Test getting user conversation history"""
    response = client.get(
        "/api/user/history",
        params={"user_id": test_user.id, "limit": 10},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "conversations" in data
    conversations = data["conversations"]
    assert len(conversations) >= 1
    
    # Check first conversation
    assert conversations[0]["id"] == test_conversation.id
    assert conversations[0]["title"] == "Test Conversation"
    assert len(conversations[0]["messages"]) == 2
    
    # Check messages
    messages = conversations[0]["messages"]
    assert messages[0]["content"] == "Hello, AI assistant!"
    assert messages[0]["is_user"] is True
    assert messages[1]["content"] == "Hello! How can I help you today?"
    assert messages[1]["is_user"] is False

@patch("app.api.chat.AIEngine")
def test_get_recommendations(mock_ai_engine, client, test_user, test_user_token):
    """Test getting proactive recommendations"""
    # Configure the mock
    mock_instance = MagicMock()
    mock_proactive = MagicMock()
    mock_proactive.generate_recommendations.return_value = [
        {"message": "Try feature X", "confidence": 0.9, "topic": "features"},
        {"message": "Would you like to learn about Y?", "confidence": 0.8, "topic": "learning"}
    ]
    mock_instance.proactive_engine = mock_proactive
    mock_ai_engine.return_value = mock_instance
    
    # Test the recommendations endpoint
    response = client.get(
        "/api/recommendations",
        params={"user_id": test_user.id},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "recommendations" in data
    recommendations = data["recommendations"]
    assert len(recommendations) == 2
    assert recommendations[0]["message"] == "Try feature X"
    assert recommendations[1]["message"] == "Would you like to learn about Y?"
