"""
Chat Functionality Tests Module

This module contains tests for the chat functionality of the advanced AI chatbot
application. It tests various chat-related features including:

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

These tests use mocked AI engine responses to ensure consistent and predictable
test results, while validating that the API endpoints correctly process and
return chat-related data.
"""

from unittest.mock import patch, MagicMock
from fastapi import status


@patch("app.api.chat.AIEngine")
def test_chat_endpoint(mock_ai_engine, client, test_user, test_user_token):
    """Test chat endpoint with mocked AI engine."""
    # Configure the mock to return a predefined response
    mock_instance = MagicMock()
    mock_instance.process_input.return_value = {
        "response": "This is a test response from the AI",
        "metadata": {
            "sentiment": {"label": "NEUTRAL", "score": 0.8},
            "topics": ["test"],
        },
        "proactive_recommendation": "Would you like to know more about testing?",
    }
    mock_ai_engine.return_value = mock_instance

    # Test the chat endpoint
    response = client.post(
        "/api/chat",
        json={
            "user_id": test_user.id,
            "message": "Hello, this is a test message",
            "conversation_id": None,  # New conversation
        },
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    if response.status_code != status.HTTP_200_OK:
        raise AssertionError("Expected status code 200 OK")

    data = response.json()

    if data["response"] != "This is a test response from the AI":
        raise AssertionError("Response mismatch")

    if "metadata" not in data:
        raise AssertionError("Metadata missing in response")

    expected_recommendation = "Would you like to know more about testing?"
    if data["proactive_recommendation"] != expected_recommendation:
        raise AssertionError("Proactive recommendation mismatch")

    if "conversation_id" not in data:
        raise AssertionError("Conversation ID missing in response")


@patch("app.api.chat.AIEngine")
def test_chat_with_existing_conversation(
    mock_ai_engine, client, test_user, test_user_token, test_conversation
):
    """Test chat endpoint with an existing conversation."""
    # Configure the mock
    mock_instance = MagicMock()
    mock_instance.process_input.return_value = {
        "response": "Follow-up response",
        "metadata": {"sentiment": {"label": "NEUTRAL", "score": 0.8}},
        "proactive_recommendation": None,
    }
    mock_ai_engine.return_value = mock_instance

    # Test the chat endpoint with existing conversation
    response = client.post(
        "/api/chat",
        json={
            "user_id": test_user.id,
            "message": "This is a follow-up message",
            "conversation_id": test_conversation.id,
        },
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    if response.status_code != status.HTTP_200_OK:
        raise AssertionError("Expected status code 200 OK")

    data = response.json()

    if data["response"] != "Follow-up response":
        raise AssertionError("Response mismatch")

    if "metadata" not in data:
        raise AssertionError("Metadata missing in response")

    if data["conversation_id"] != test_conversation.id:
        raise AssertionError("Conversation ID mismatch")


def test_get_user_history(client, test_user, test_user_token, test_conversation):
    """Test getting user conversation history."""
    response = client.post(
        "/api/user/history",
        json={"user_id": test_user.id, "limit": 5},
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    if response.status_code != status.HTTP_200_OK:
        raise AssertionError("Expected status code 200 OK")

    data = response.json()

    if "conversations" not in data:
        raise AssertionError("Conversations missing in response")

    if len(data["conversations"]) == 0:
        raise AssertionError("No conversations returned")

    conversation = data["conversations"][0]
    if "id" not in conversation or "messages" not in conversation:
        raise AssertionError("Invalid conversation structure")

    if len(conversation["messages"]) == 0:
        raise AssertionError("No messages in conversation")


@patch("app.api.chat.AIEngine")
def test_get_recommendations(mock_ai_engine, client, test_user, test_user_token):
    """Test getting proactive recommendations."""
    # Configure the mock
    mock_instance = MagicMock()
    mock_proactive = MagicMock()
    mock_proactive.generate_recommendations.return_value = [
        {
            "text": "Would you like to explore machine learning?",
            "confidence": 0.85,
            "category": "education",
        },
        {
            "text": "Check out our new voice features!",
            "confidence": 0.75,
            "category": "feature",
        },
    ]
    mock_instance.proactive_engine = mock_proactive
    mock_ai_engine.return_value = mock_instance

    # Test the recommendations endpoint
    response = client.post(
        "/api/recommendations",
        json={"user_id": test_user.id},
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    if response.status_code != status.HTTP_200_OK:
        raise AssertionError("Expected status code 200 OK")

    data = response.json()

    if "recommendations" not in data:
        raise AssertionError("Recommendations missing in response")

    if len(data["recommendations"]) != 2:
        raise AssertionError("Expected 2 recommendations")

    rec = data["recommendations"][0]
    if "text" not in rec or "confidence" not in rec or "category" not in rec:
        raise AssertionError("Invalid recommendation structure")
