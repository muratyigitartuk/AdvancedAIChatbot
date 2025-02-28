"""
User Profile Service Module

This module provides services for managing user profiles, conversations, and topics.
It serves as an abstraction layer between the application logic and the database,
handling all user-related data operations.
"""

from app.db.models import User, Conversation, Message, UserTopic
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import datetime

class UserProfileService:
    """
    Service for managing user profiles, conversations, and topics.
    
    This service provides methods for:
    - Retrieving user conversation history
    - Creating and managing conversations
    - Tracking user topics of interest
    - Updating user preferences
    
    It serves as an interface between the application logic and the database,
    encapsulating all user-related data operations.
    
    Attributes:
        db (Session): SQLAlchemy database session
    """
    def __init__(self, db: Session):
        """
        Initialize the UserProfileService with a database session.
        
        Args:
            db (Session): SQLAlchemy database session
        """
        self.db = db
    
    def get_user_history(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent user conversation history.
        
        Retrieves the most recent conversations for a user, including all messages
        within those conversations, ordered by the most recently updated first.
        
        Args:
            user_id (int): The ID of the user
            limit (int, optional): Maximum number of conversations to return. Defaults to 10.
            
        Returns:
            List[Dict[str, Any]]: List of conversation objects with their messages
        """
        conversations = (
            self.db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
            .all()
        )
        
        result = []
        for conv in conversations:
            messages = (
                self.db.query(Message)
                .filter(Message.conversation_id == conv.id)
                .order_by(Message.created_at)
                .all()
            )
            
            result.append({
                "id": conv.id,
                "title": conv.title,
                "created_at": conv.created_at,
                "messages": [
                    {
                        "id": msg.id,
                        "content": msg.content,
                        "is_user": msg.is_user,
                        "created_at": msg.created_at.isoformat(),
                        "metadata": msg.metadata
                    }
                    for msg in messages
                ]
            })
        
        return result
    
    def get_user_topics(self, user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get topics of interest for a user.
        
        Retrieves the topics of interest for a user, ordered by their weight in descending order.
        
        Args:
            user_id (int): The ID of the user
            limit (int, optional): Maximum number of topics to return. Defaults to 20.
            
        Returns:
            List[Dict[str, Any]]: List of topic objects
        """
        topics = (
            self.db.query(UserTopic)
            .filter(UserTopic.user_id == user_id)
            .order_by(UserTopic.weight.desc())
            .limit(limit)
            .all()
        )
        
        return [
            {
                "topic": topic.topic,
                "weight": topic.weight,
                "last_mentioned": topic.last_mentioned
            }
            for topic in topics
        ]
    
    def update_user_preferences(self, user_id: int, preferences: Dict[str, Any]) -> None:
        """
        Update user preferences.
        
        Updates the preferences for a user by merging the new preferences with the existing ones.
        
        Args:
            user_id (int): The ID of the user
            preferences (Dict[str, Any]): New preferences to update
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            # Merge the new preferences with existing ones
            updated_prefs = {**user.preferences, **preferences}
            user.preferences = updated_prefs
            self.db.commit()
    
    def add_user_message(self, user_id: int, conversation_id: int, content: str, metadata: Dict[str, Any] = None) -> Message:
        """
        Add a user message to a conversation.
        
        Creates a new message in a conversation and associates it with the user.
        
        Args:
            user_id (int): The ID of the user
            conversation_id (int): The ID of the conversation
            content (str): The content of the message
            metadata (Dict[str, Any], optional): Metadata for the message. Defaults to None.
            
        Returns:
            Message: The newly created message
        """
        message = Message(
            conversation_id=conversation_id,
            content=content,
            is_user=True,
            metadata=metadata or {}
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def add_bot_message(self, conversation_id: int, content: str, metadata: Dict[str, Any] = None) -> Message:
        """
        Add a bot message to a conversation.
        
        Creates a new message in a conversation and associates it with the bot.
        
        Args:
            conversation_id (int): The ID of the conversation
            content (str): The content of the message
            metadata (Dict[str, Any], optional): Metadata for the message. Defaults to None.
            
        Returns:
            Message: The newly created message
        """
        message = Message(
            conversation_id=conversation_id,
            content=content,
            is_user=False,
            metadata=metadata or {}
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def create_conversation(self, user_id: int, title: str = None) -> Conversation:
        """
        Create a new conversation for a user.
        
        Creates a new conversation and associates it with the user.
        
        Args:
            user_id (int): The ID of the user
            title (str, optional): The title of the conversation. Defaults to None.
            
        Returns:
            Conversation: The newly created conversation
        """
        conversation = Conversation(
            user_id=user_id,
            title=title or f"Conversation {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation
    
    def update_user_topics(self, user_id: int, detected_topics: List[str]) -> None:
        """
        Update user topics based on newly detected topics.
        
        Updates the topics of interest for a user by incrementing the weight of existing topics
        and adding new topics.
        
        Args:
            user_id (int): The ID of the user
            detected_topics (List[str]): List of newly detected topics
        """
        for topic_name in detected_topics:
            # Check if topic already exists
            topic = (
                self.db.query(UserTopic)
                .filter(
                    UserTopic.user_id == user_id,
                    UserTopic.topic == topic_name
                )
                .first()
            )
            
            if topic:
                # Update existing topic
                topic.weight += 1
                topic.last_mentioned = datetime.datetime.utcnow()
            else:
                # Create new topic
                topic = UserTopic(
                    user_id=user_id,
                    topic=topic_name,
                    weight=1,
                    last_mentioned=datetime.datetime.utcnow()
                )
                self.db.add(topic)
        
        self.db.commit()
