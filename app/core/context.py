"""
Context Builder Module

This module provides functionality for building conversational context
for the AI chatbot. It processes user conversation history, preferences,
and topics to create a rich context that helps the AI generate more
personalized and contextually relevant responses.
"""

from app.services.user_profile import UserProfileService
from typing import Dict, List, Any, Optional
import datetime
import os


class ContextBuilder:
    """
    Builds and manages conversational context for AI response generation.

    The ContextBuilder is responsible for gathering relevant information about
    the user and their conversation history, and formatting it into a context
    prompt that can be used by the AI model to generate appropriate responses.

    It handles:
    - Retrieving and formatting conversation history
    - Including user preferences and topics of interest
    - Managing context length to fit within token limits
    - Structuring the context in a format optimal for the AI model

    Attributes:
        user_profile_service (UserProfileService): Service for accessing user data
        max_history_items (int): Maximum number of conversation turns to include
        max_tokens (int): Maximum token length for the context
    """

    def __init__(
        self,
        user_profile_service: UserProfileService,
        max_history_items: int = 10,
        max_tokens: int = 4000,
    ):
        """
        Initialize the ContextBuilder with configuration parameters.

        Args:
            user_profile_service (UserProfileService): Service for accessing user data
            max_history_items (int, optional): Maximum conversation turns to include. Defaults to 10.
            max_tokens (int, optional): Maximum token length for context. Defaults to 4000.
        """
        self.user_profile_service = user_profile_service
        self.max_history_items = max_history_items
        self.max_tokens = max_tokens

    def build_context(
        self, user_id: int, conversation_id: int, current_message: str
    ) -> str:
        """
        Build a complete context for AI response generation.

        This method gathers all relevant information about the user and their
        conversation history, and formats it into a context prompt for the AI model.

        Args:
            user_id (int): ID of the user
            conversation_id (int): ID of the current conversation
            current_message (str): The user's current message

        Returns:
            str: Formatted context prompt for the AI model
        """
        # Get user conversation history
        conversation_history = self._get_conversation_history(conversation_id)

        # Get user topics
        user_topics = self.user_profile_service.get_user_topics(user_id)

        # Get user preferences
        user_preferences = self._get_user_preferences(user_id)

        # Create context prompt
        context = self._format_context(
            current_message, conversation_history, user_topics, user_preferences
        )

        return context

    def _get_conversation_history(
        self, conversation_id: int
    ) -> List[Dict[str, Any]]:
        """
        Retrieve conversation history for the current conversation.

        Args:
            conversation_id (int): ID of the conversation to retrieve

        Returns:
            List[Dict[str, Any]]: List of message objects with content and metadata
        """
        # Query the conversation using SQLAlchemy ORM
        from app.db.models import Conversation, Message

        # Get the conversation
        conversation = (
            self.user_profile_service.db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )

        if not conversation:
            return []

        # Get messages
        messages = []
        for msg in conversation.messages:
            messages.append(
                {
                    "content": msg.content,
                    "is_user": msg.is_user,
                    "timestamp": msg.created_at,
                }
            )

        # Sort by timestamp and take the most recent N messages
        messages.sort(key=lambda x: x["timestamp"])

        return messages[-self.max_history_items:]

    def _get_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """
        Retrieve user preferences.

        Args:
            user_id (int): ID of the user

        Returns:
            Dict[str, Any]: Dictionary of user preferences
        """
        user = self.user_profile_service.db.query("User").filter_by(id=user_id).first()
        if user:
            return user.get("preferences", {})
        return {}

    def _format_context(
        self,
        current_message: str,
        conversation_history: List[Dict[str, Any]],
        user_topics: List[Dict[str, Any]],
        user_preferences: Dict[str, Any],
    ) -> str:
        """
        Format context for the AI model.

        This method takes the gathered information and structures it into a
        context prompt that can be used by the AI model to generate a response.

        Args:
            current_message (str): The user's current message
            conversation_history (List[Dict[str, Any]]): List of conversation history messages
            user_topics (List[Dict[str, Any]]): List of user topics
            user_preferences (Dict[str, Any]): Dictionary of user preferences

        Returns:
            str: Formatted context prompt for the AI model
        """
        # Start with system instruction
        context = (
            "You are a helpful assistant that learns from user interactions. "
            "You should tailor your responses based on the user's history "
            "and preferences. "
        )

        # Add user preferences if available
        if user_preferences:
            context += "The user has the following preferences: "
            for key, value in user_preferences.items():
                context += f"{key}: {value}, "
            context = context.rstrip(", ") + ". "

        # Add user topics if available
        if user_topics:
            context += "The user has shown interest in the following topics: "
            # Sort topics by weight, descending
            sorted_topics = sorted(
                user_topics, key=lambda x: x["weight"], reverse=True
            )
            # Take top 5 topics
            top_topics = sorted_topics[:5]
            context += ", ".join([t["topic"] for t in top_topics]) + ". "

        # Add conversation history
        if conversation_history:
            context += "Here's the recent conversation history: "
            for msg in conversation_history:
                role = "User" if msg["is_user"] else "Assistant"
                content = msg["content"]
                context += f"\n{role}: {content}"

        # Add current message
        context += f"\nUser: {current_message}\nAssistant: "

        return context
