# models/feedback.py
import datetime
from config.db import DatabaseConnection

class FeedbackModel:
    def __init__(self):
        self.db = DatabaseConnection().get_db()
        self.collection = self.db['feedback']
        
        # Create indexes
        self.collection.create_index([("conversation_id", 1)], unique=True)
    
    def save_feedback(self, conversation_id, rating, comments=None, helpful=True):
        """Save user feedback for a response"""
        feedback = {
            "conversation_id": conversation_id,
            "rating": rating,  # 1-5 scale
            "helpful": helpful,
            "comments": comments,
            "timestamp": datetime.datetime.now()
        }
        
        # Use upsert to update if exists or insert if not
        result = self.collection.update_one(
            {"conversation_id": conversation_id},
            {"$set": feedback},
            upsert=True
        )
        
        return result.acknowledged
    
    def get_feedback_stats(self):
        """Get overall feedback statistics"""
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "average_rating": {"$avg": "$rating"},
                    "helpful_count": {
                        "$sum": {"$cond": [{"$eq": ["$helpful", True]}, 1, 0]}
                    },
                    "total_count": {"$sum": 1}
                }
            }
        ]
        
        result = list(self.collection.aggregate(pipeline))
        if result:
            stats = result[0]
            stats["helpful_percentage"] = (stats["helpful_count"] / stats["total_count"]) * 100 if stats["total_count"] > 0 else 0
            return stats
        return {"average_rating": 0, "helpful_count": 0, "total_count": 0, "helpful_percentage": 0}