from typing import List, Dict, Any
from app.services.user_profile import UserProfileService
import datetime
from app.db.models import User


class ProactiveEngine:
    def __init__(self, user_profile_service: UserProfileService):
        self.user_profile_service = user_profile_service

    def generate_recommendations(self, user_id: int) -> List[Dict[str, Any]]:
        """Generate proactive recommendations based on user history and topics"""
        # Get user topics of interest
        topics = self.user_profile_service.get_user_topics(user_id)

        # Get user recent history
        history = self.user_profile_service.get_user_history(user_id)

        # Analyze patterns and generate recommendations
        recommendations = []

        # Example: Check for recurring questions about the same topic
        topic_frequency = {}
        for conv in history:
            for msg in conv["messages"]:
                if msg["is_user"] and msg.get("message_metadata") and msg["message_metadata"].get("topics"):
                    for topic in msg["message_metadata"]["topics"]:
                        topic_frequency[topic] = topic_frequency.get(topic, 0) + 1

        # Recommend topics that are frequently asked about
        for topic, freq in topic_frequency.items():
            if freq >= 3:  # If asked 3+ times about the same topic
                recommendations.append(
                    {
                        "type": "frequent_topic",
                        "topic": topic,
                        "message": f"I notice you've asked about {topic} several times. Would you like more comprehensive information about it?",
                    }
                )

        # Example: Check for time-based recommendations
        now = datetime.datetime.utcnow()
        for topic in topics:
            # If topic was last mentioned more than 7 days ago but is important
            days_since = (now - topic["last_mentioned"]).days
            if days_since > 7 and topic["weight"] > 5:
                recommendations.append(
                    {
                        "type": "reminder",
                        "topic": topic["topic"],
                        "message": f"It's been a while since we discussed {topic['topic']}. Any updates or questions on that front?",
                    }
                )

        # Example: Detect potential follow-up questions
        if history:
            last_conversation = history[0]
            if last_conversation["messages"]:
                last_message = last_conversation["messages"][-1]
                if not last_message["is_user"]:  # If last message was from bot
                    # Check if it was about a topic that tends to have follow-ups
                    if (
                        last_message.get("message_metadata")
                        and last_message["message_metadata"].get("topics")
                        and "technology" in last_message["message_metadata"]["topics"]
                    ):
                        recommendations.append(
                            {
                                "type": "follow_up",
                                "topic": "technology",
                                "message": "Would you like me to explain more about how this technology works?",
                            }
                        )

        return recommendations[:3]  # Limit to top 3 recommendations

    def should_send_recommendation(self, user_id: int) -> bool:
        """Determine if we should send a proactive recommendation now"""
        # Get user preferences
        user = self.user_profile_service.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        preferences = user.preferences

        # Check if user has disabled proactive recommendations
        if preferences.get("disable_proactive", False):
            return False

        # Check frequency setting
        frequency = preferences.get("recommendation_frequency", "medium")

        # Check last recommendation time
        last_recommendation_time = preferences.get("last_recommendation_time")
        now = datetime.datetime.utcnow()

        if last_recommendation_time:
            last_time = datetime.datetime.fromisoformat(last_recommendation_time)
            hours_since = (now - last_time).total_seconds() / 3600

            # Apply frequency rules
            if frequency == "low" and hours_since < 24:  # Once a day
                return False
            elif frequency == "medium" and hours_since < 6:  # ~4 times a day
                return False
            elif frequency == "high" and hours_since < 1:  # Every hour
                return False

        # Update last recommendation time
        preferences["last_recommendation_time"] = now.isoformat()
        user.preferences = preferences
        self.user_profile_service.db.commit()

        return True
