from typing import Dict, List, Any, Optional
import os
import openai
import time
from app.core.context import ContextBuilder
from app.core.proactive import ProactiveEngine
from app.services.user_profile import UserProfileService


class AIEngine:
    """
    Core AI engine that handles natural language processing, context management,
    and generation of responses for the chatbot.

    This class integrates with OpenAI's API and Hugging Face Transformers to provide
    advanced NLP capabilities including sentiment analysis, entity recognition,
    and contextual response generation. It also supports proactive recommendations
    based on user conversation history.

    Attributes:
        user_profile_service (UserProfileService): Service for managing user profiles and history
        context_builder (ContextBuilder): Utility for building context from conversation history
        proactive_engine (ProactiveEngine): Engine for generating proactive recommendations
        model (str): The OpenAI model to use for generating responses
        openai_api_key (str): API key for OpenAI services
        sentiment_analyzer: Pipeline for sentiment analysis
        entity_recognizer: Pipeline for named entity recognition
    """

    def __init__(
        self,
        user_profile_service: UserProfileService,
        context_builder: ContextBuilder,
        proactive_engine: Optional[ProactiveEngine] = None,
        model: str = None,
    ):
        """
        Initialize the AI Engine with required services and components.

        Args:
            user_profile_service (UserProfileService): Service for managing user profiles
            context_builder (ContextBuilder): Utility for building conversation context
            proactive_engine (Optional[ProactiveEngine]): Engine for proactive recommendations
            model (str, optional): OpenAI model name. Defaults to environment variable or "gpt-3.5-turbo"
        """
        self.user_profile_service = user_profile_service
        self.context_builder = context_builder
        self.proactive_engine = proactive_engine
        self.model = model or os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # Initialize NLP components
        self._init_nlp_components()

        # Set OpenAI API key
        openai.api_key = self.openai_api_key

    def _init_nlp_components(self):
        """
        Initialize NLP components for sentiment analysis and entity recognition.

        This method attempts to load Hugging Face Transformers pipelines for NLP tasks.
        If the transformers library is not available, it falls back to dummy implementations.
        """
        try:
            from transformers import pipeline

            # Initialize sentiment analysis pipeline
            self.sentiment_analyzer = pipeline("sentiment-analysis")

            # Initialize entity recognition pipeline
            self.entity_recognizer = pipeline("ner")
        except ImportError:
            print(
                "Warning: Transformers library not available. "
                "Using dummy NLP components."
            )
            # Create dummy NLP components for systems without transformers
            self.sentiment_analyzer = self._dummy_sentiment_analyzer
            self.entity_recognizer = self._dummy_entity_recognizer

    def _dummy_sentiment_analyzer(self, text):
        """
        Dummy sentiment analyzer for systems without transformers.

        Returns a neutral sentiment score.

        Args:
            text (str): Input text for sentiment analysis
        Returns:
            List[Dict[str, Any]]: Sentiment analysis result
        """
        # Return neutral sentiment
        return [{"label": "NEUTRAL", "score": 0.5}]

    def _dummy_entity_recognizer(self, text):
        """
        Dummy entity recognizer for systems without transformers.

        Returns an empty list of entities.

        Args:
            text (str): Input text for entity recognition
        Returns:
            List[Dict[str, Any]]: Entity recognition result
        """
        # Return empty entities list
        return []

    def process_input(
        self, user_id: int, conversation_id: int, message: str
    ) -> Dict[str, Any]:
        """
        Process user input and generate a response.

        This method analyzes the input message for metadata, updates user topics,
        builds conversation context, generates a response using the AI model,
        and checks for proactive recommendations.

        Args:
            user_id (int): Unique identifier for the user
            conversation_id (int): Unique identifier for the conversation
            message (str): User input message
        Returns:
            Dict[str, Any]: Response and metadata
        """
        # Analyze message for metadata
        message_metadata = self._analyze_message(message)

        # Update user topics based on extracted topics
        if message_metadata.get("topics"):
            self.user_profile_service.update_user_topics(
                user_id, message_metadata["topics"]
            )

        # Build context from user history
        context = self.context_builder.build_context(user_id, conversation_id, message)
        # Start timing the response
        start_time = time.time()

        # Generate response from AI model
        response = self._generate_response(context)

        # Check for proactive recommendations
        proactive_recommendation = None
        if self.proactive_engine and self.proactive_engine.should_send_recommendation(
            user_id
        ):
            recommendations = self.proactive_engine.generate_recommendations(user_id)
            if recommendations:
                proactive_recommendation = recommendations[0]["message"]

        # Add user message to conversation
        self.user_profile_service.add_user_message(
            user_id, conversation_id, message, message_metadata
        )

        # Add bot message to conversation
        self.user_profile_service.add_bot_message(
            conversation_id,
            response,
            {
                "response_time": time.time() - start_time,
                "ai_model": self.model,
            },
        )

        return {
            "response": response,
            "message_metadata": message_metadata,
            "conversation_id": conversation_id,
            "proactive_recommendation": proactive_recommendation,
        }

    def _analyze_message(self, message: str) -> Dict[str, Any]:
        """
        Analyze message for sentiment, entities, and topics.

        Args:
            message (str): Input message for analysis
        Returns:
            Dict[str, Any]: Analysis result
        """
        # Perform sentiment analysis
        sentiment = self.sentiment_analyzer(message)[0]

        # Extract entities
        entities = self._extract_entities(message)

        # Extract topics
        topics = self._extract_topics(message)

        return {
            "sentiment": {"label": sentiment["label"], "score": sentiment["score"]},
            "entities": entities,
            "topics": topics,
        }

    def _extract_entities(self, message: str) -> List[Dict[str, Any]]:
        """
        Extract named entities from message.

        Args:
            message (str): Input message for entity extraction
        Returns:
            List[Dict[str, Any]]: Extracted entities
        """
        entities = self.entity_recognizer(message)

        # Group entities that span multiple tokens
        grouped_entities = []
        current_entity = None

        for entity in entities:
            if (
                current_entity
                and entity["entity"].startswith("I-")
                and current_entity["entity"] == entity["entity"].replace("I-", "B-")
            ):
                # Continue the current entity
                current_entity["word"] += " " + entity["word"]
                current_entity["end"] = entity["end"]
            else:
                # Start a new entity
                if current_entity:
                    grouped_entities.append(current_entity)

                current_entity = {
                    "entity": entity["entity"],
                    "word": entity["word"],
                    "start": entity["start"],
                    "end": entity["end"],
                    "score": entity["score"],
                }

        if current_entity:
            grouped_entities.append(current_entity)

        return grouped_entities

    def _extract_topics(self, message: str) -> List[str]:
        """
        Extract topics from message - simplified example.

        This method uses a simple keyword-based approach for topic extraction.
        In a real-world application, a more sophisticated topic modeling approach
        would be used.

        Args:
            message (str): Input message for topic extraction
        Returns:
            List[str]: Extracted topics
        """
        # This would typically use a topic modeling approach
        # For simplicity, using keywords as a placeholder
        keywords = [
            "finance",
            "health",
            "technology",
            "travel",
            "food",
            "education",
            "sports",
            "entertainment",
            "news",
            "weather",
        ]

        message_lower = message.lower()
        found_topics = [topic for topic in keywords if topic in message_lower]

        return found_topics

    def _generate_response(self, context: str) -> str:
        """
        Generate response using AI model.

        This method uses the OpenAI API to generate a response based on the
        input context.

        Args:
            context (str): Input context for response generation
        Returns:
            str: Generated response
        """
        try:
            # Using OpenAI API for response generation
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that learns "
                        "from user interactions.",
                    },
                    {"role": "user", "content": context},
                ],
                max_tokens=500,
                temperature=0.7,
            )

            return response.choices[0].message["content"]
        except Exception as e:
            print(f"Error generating response from OpenAI: {e}")
            # Fallback to a simple response
            return (
                "I'm sorry, I'm having trouble generating a response right now. "
                "Please try again later."
            )
