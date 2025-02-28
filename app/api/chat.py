"""
Chat API Module

This module provides the API endpoints for chat functionality, including:
- Processing chat messages and generating AI responses
- Retrieving user conversation history
- Generating proactive recommendations based on user history

The module defines Pydantic models for request/response validation and
implements FastAPI route handlers for each endpoint.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.db.database import get_db
from app.services.user_profile import UserProfileService
from app.core.ai_engine import AIEngine
from app.core.context import ContextBuilder
from app.core.proactive import ProactiveEngine

router = APIRouter()

# Request and response models
class ChatRequest(BaseModel):
    """
    Request model for chat messages.
    
    Attributes:
        user_id (int): The ID of the user sending the message
        message (str): The content of the user's message
        conversation_id (Optional[int]): The ID of the existing conversation, or None to create a new one
    """
    user_id: int
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    """
    Response model for chat messages.
    
    Attributes:
        response (str): The AI-generated response text
        metadata (Dict[str, Any]): Additional information about the response (sentiment, entities, etc.)
        proactive_recommendation (Optional[str]): A proactive suggestion based on user history, if available
        conversation_id (int): The ID of the conversation this message belongs to
    """
    response: str
    metadata: Dict[str, Any]
    proactive_recommendation: Optional[str] = None
    conversation_id: int

class UserHistoryRequest(BaseModel):
    """
    Request model for retrieving user conversation history.
    
    Attributes:
        user_id (int): The ID of the user whose history to retrieve
        limit (Optional[int]): Maximum number of conversations to return, defaults to 10
    """
    user_id: int
    limit: Optional[int] = 10

class ConversationModel(BaseModel):
    """
    Model representing a conversation with its messages.
    
    Attributes:
        id (int): The unique identifier for the conversation
        title (str): The title of the conversation
        created_at (str): The timestamp when the conversation was created
        messages (List[Dict[str, Any]]): The list of messages in the conversation
    """
    id: int
    title: str
    created_at: str
    messages: List[Dict[str, Any]]

class UserHistoryResponse(BaseModel):
    """
    Response model for user conversation history.
    
    Attributes:
        conversations (List[ConversationModel]): List of user's conversations
    """
    conversations: List[ConversationModel]

class RecommendationRequest(BaseModel):
    """
    Request model for retrieving proactive recommendations.
    
    Attributes:
        user_id (int): The ID of the user to generate recommendations for
    """
    user_id: int

class RecommendationResponse(BaseModel):
    """
    Response model for proactive recommendations.
    
    Attributes:
        recommendations (List[Dict[str, Any]]): List of recommendations with their details
    """
    recommendations: List[Dict[str, Any]]

# Dependency to get AI engine
def get_ai_engine(db: Session = Depends(get_db)):
    """
    Dependency that creates and returns an AIEngine instance.
    
    This function initializes all the necessary components for the AI engine,
    including the user profile service, context builder, and proactive engine.
    
    Args:
        db (Session): Database session dependency
        
    Returns:
        AIEngine: Configured AI engine instance
    """
    user_profile_service = UserProfileService(db)
    context_builder = ContextBuilder(user_profile_service)
    proactive_engine = ProactiveEngine(user_profile_service)
    return AIEngine(user_profile_service, context_builder, proactive_engine)

@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    ai_engine: AIEngine = Depends(get_ai_engine),
    db: Session = Depends(get_db)
):
    """
    Process a chat message and return an AI-generated response.
    
    This endpoint handles incoming user messages, processes them through the AI engine,
    and returns the generated response along with metadata and any proactive recommendations.
    If no conversation_id is provided, a new conversation will be created.
    
    Args:
        request (ChatRequest): The chat request containing user ID, message, and optional conversation ID
        ai_engine (AIEngine): The AI engine dependency for processing the message
        db (Session): Database session dependency
        
    Returns:
        ChatResponse: The AI response with metadata and conversation information
    """
    user_profile_service = UserProfileService(db)
    
    # Create a new conversation if needed
    conversation_id = request.conversation_id
    if not conversation_id:
        conversation = user_profile_service.create_conversation(request.user_id)
        conversation_id = conversation.id
    
    # Process the message
    result = ai_engine.process_input(
        request.user_id,
        conversation_id,
        request.message
    )
    
    return {
        "response": result["response"],
        "metadata": result["metadata"],
        "proactive_recommendation": result["proactive_recommendation"],
        "conversation_id": conversation_id
    }

@router.get("/user/history", response_model=UserHistoryResponse)
def get_user_history(
    request: UserHistoryRequest,
    db: Session = Depends(get_db)
):
    """
    Retrieve conversation history for a user.
    
    This endpoint returns a list of the user's conversations, including
    the messages within each conversation, up to the specified limit.
    
    Args:
        request (UserHistoryRequest): The request containing user ID and optional limit
        db (Session): Database session dependency
        
    Returns:
        UserHistoryResponse: The user's conversation history
    """
    user_profile_service = UserProfileService(db)
    history = user_profile_service.get_user_history(request.user_id, request.limit)
    
    return {"conversations": history}

@router.get("/recommendations", response_model=RecommendationResponse)
def get_recommendations(
    request: RecommendationRequest,
    ai_engine: AIEngine = Depends(get_ai_engine)
):
    """
    Generate proactive recommendations for a user.
    
    This endpoint analyzes the user's conversation history and preferences
    to generate personalized recommendations that might be relevant to them.
    
    Args:
        request (RecommendationRequest): The request containing the user ID
        ai_engine (AIEngine): The AI engine dependency for generating recommendations
        
    Returns:
        RecommendationResponse: A list of proactive recommendations
    """
    recommendations = ai_engine.proactive_engine.generate_recommendations(request.user_id)
    
    return {"recommendations": recommendations}
