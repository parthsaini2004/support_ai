# models/user_query.py
from config.db import DatabaseConnection
from pymongo.errors import PyMongoError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserModel:
    def __init__(self):
        self.db = DatabaseConnection().get_db()
        self.users = self.db['users']
        self.orders = self.db['orders']
    
    def get_user_by_id(self, user_id):
        """Get user information by user ID"""
        try:
            return self.users.find_one({"user_id": int(user_id)}, {"password": 0})
        except PyMongoError as e:
            logger.error(f"Error fetching user: {e}")
            return None
    
    def get_user_orders(self, user_id):
        """Get orders for a specific user"""
        try:
            return list(self.orders.find({"user_id": int(user_id)}))
        except PyMongoError as e:
            logger.error(f"Error fetching orders: {e}")
            return []
    
    def get_order_by_id(self, order_id):
        """Get order by order ID"""
        try:
            return self.orders.find_one({"order_id": int(order_id)})
        except PyMongoError as e:
            logger.error(f"Error fetching order: {e}")
            return None
    
    def get_refund_status(self, order_id):
        """Get refund status for an order"""
        try:
            order = self.orders.find_one(
                {"order_id": int(order_id)},
                {"refund": 1, "order_date": 1}
            )
            
            if not order:
                return None
                
            # Check if order is refundable
            current_date = datetime.datetime.now()
            if order.get("refund", {}).get("refundable", False):
                refundable_within = order.get("refund", {}).get("refundable_within")
                is_refundable = refundable_within and current_date <= refundable_within
                
                return {
                    "is_refundable": is_refundable,
                    "refundable_within": refundable_within,
                    "days_left": (refundable_within - current_date).days if is_refundable else 0
                }
            
            return {"is_refundable": False}
            
        except PyMongoError as e:
            logger.error(f"Error fetching refund status: {e}")
            return None