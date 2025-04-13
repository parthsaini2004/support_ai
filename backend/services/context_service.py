# services/context_service.py
import json
from models.conversation import ConversationModel
from models.user_query import UserModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContextService:
    def __init__(self):
        self.conversation_model = ConversationModel()
        self.user_model = UserModel()
        
    def build_context(self, user_id, query):
        """Build context for AI response generation"""
        try:
            # Get user information
            user_info = self.user_model.get_user_by_id(user_id)
            
            # Get conversation history
            conversation_history = self.conversation_model.get_conversation_history(user_id, limit=3)
            
            # Get user orders (limited to recent/active orders)
            user_orders = self.user_model.get_user_orders(user_id)
            
            # Parse query to identify any order-specific information
            mentioned_order_ids = self._extract_order_ids(query)
            order_details = []
            
            # Get specific order information if mentioned in the query
            if mentioned_order_ids:
                for order_id in mentioned_order_ids:
                    order = self.user_model.get_order_by_id(order_id)
                    if order:
                        order_details.append(order)
            
            # Build context object
            context = {
                "user": {
                    "user_id": user_info.get("user_id") if user_info else None,
                    "username": user_info.get("username") if user_info else None,
                    "email": user_info.get("email") if user_info else None,
                    "id_creation_date": user_info.get("id_creation_date") if user_info else None
                },
                "conversation_history": [
                    {
                        "query": conv.get("query"),
                        "response": conv.get("response"),
                        "timestamp": conv.get("timestamp").isoformat()
                    } for conv in conversation_history
                ],
                "orders": [
                    {
                        "order_id": order.get("order_id"),
                        "status": order.get("status"),
                        "completed": order.get("completed"),
                        "order_date": order.get("order_date").isoformat() if order.get("order_date") else None,
                        "price": order.get("price"),
                        "description": order.get("description"),
                        "refund": order.get("refund")
                    } for order in (order_details if order_details else user_orders[:3])
                ]
            }
            
            return json.dumps(context, default=str)
            
        except Exception as e:
            logger.error(f"Error building context: {e}")
            return json.dumps({"error": "Failed to build context"})
    
    def _extract_order_ids(self, query):
        """Extract order IDs mentioned in the query using simple regex"""
        import re
        
        # Find patterns like "order 12345" or "order #12345" or "order-12345"
        order_patterns = [
            r"order\s+#?(\d+)",
            r"order[-\s]?id\s+#?(\d+)",
            r"#(\d+)",
            r"order number\s+(\d+)"
        ]
        
        order_ids = []
        for pattern in order_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            order_ids.extend(matches)
        
        # Convert to integers and remove duplicates
        return list(set([int(order_id) for order_id in order_ids if order_id.isdigit()]))