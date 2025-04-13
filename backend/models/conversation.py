# models/conversation.py
import datetime
from pymongo import DESCENDING
from config.db import DatabaseConnection

class ConversationModel:
    def __init__(self):
        self.db = DatabaseConnection().get_db()
        self.collection = self.db['conversations']
        
        # Create indexes
        self.collection.create_index([("user_id", 1)])
        self.collection.create_index([("timestamp", DESCENDING)])
    
    def create_conversation(self, user_id, query, response, related_orders=None):
        """Create a new conversation entry"""
        conversation = {
            "user_id": user_id,
            "query": query,
            "response": response,
            "related_orders": related_orders or [],
            "timestamp": datetime.datetime.now(),
            "feedback": None
        }
        
        result = self.collection.insert_one(conversation)
        return str(result.inserted_id)
    
    def get_conversation_history(self, user_id, limit=5):
        """Get conversation history for a specific user"""
        return list(self.collection.find(
            {"user_id": user_id},
            {"_id": 0}
        ).sort("timestamp", DESCENDING).limit(limit))
    
    def update_feedback(self, conversation_id, feedback):
        """Update feedback for a conversation"""
        from bson.objectid import ObjectId
        result = self.collection.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"feedback": feedback}}
        )
        return result.modified_count > 0