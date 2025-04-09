import sys
import os
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
from pymongo import MongoClient

# 🌱 Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")

# 🔗 Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["orderAi"]
orders_collection = db["orders"]

# 📦 Fetch order info by order_id and user_id
def fetch_order_info(order_id: int, user_id: int) -> str:
    print(f"📂 Using DB: {db.name}, Collection: {orders_collection.name}", file=sys.stderr)
    print(f"🔢 Total Orders: {orders_collection.count_documents({})}", file=sys.stderr)

    # 🔍 Print all orders for inspection
    for doc in orders_collection.find():
        print(f"📄 Order Document: {doc}", file=sys.stderr)

    # 🔧 Ensure inputs are integers
    try:
        order_id = int(order_id)
        user_id = int(user_id)
    except Exception as e:
        print(f"⚠️ ID conversion failed: {e}", file=sys.stderr)
        return f"❌ Invalid order ID or user ID."

    query = {
        "order_id": order_id,
        "user_id": user_id
    }
    print(f"📦 Query Dict: {query}", file=sys.stderr)

    try:
        order = orders_collection.find_one(query)
    except Exception as e:
        print(f"⚠️ Query error: {e}", file=sys.stderr)
        order = None

    print(f"🧾 Fetched Order: {order}", file=sys.stderr)

    if not order:
        return f"❌ No order found with ID {order_id} for user ."
        # {user_id}
    status = order.get("status", {})
    delivery_date = status.get("delivery_date")
    expected_date = status.get("expected_delivery_date")
    dispatch_date = status.get("dispatch_date")

    description = order.get("description", "No description available")
    price = order.get("price", "N/A")
    completed = order.get("completed", False)
    refundable = order.get("refund", {}).get("refundable", False)

    def fmt(date_val):
        try:
            if isinstance(date_val, str):
                date_val = datetime.fromisoformat(date_val.replace("Z", "+00:00"))
            if isinstance(date_val, datetime):
                if date_val.tzinfo is None:
                    date_val = date_val.replace(tzinfo=timezone.utc)
                return date_val.strftime("%B %d, %Y")
        except Exception as e:
            print(f"⚠️ Date format error: {e}", file=sys.stderr)
        return "Not available"

    try:
        now = datetime.now(timezone.utc)
        if expected_date:
            if isinstance(expected_date, str):
                expected = datetime.fromisoformat(expected_date.replace("Z", "+00:00"))
            elif isinstance(expected_date, datetime):
                expected = expected_date
                if expected.tzinfo is None:
                    expected = expected.replace(tzinfo=timezone.utc)

            if expected < now and not delivery_date:
                return (
                    f"🚚 **Order #{order_id}** is delayed due to unforeseen circumstances like rain or logistics issues.\n"
                    f"- Expected by: {fmt(expected)}\n"
                    f"- It has not been delivered yet. We're sorry for the inconvenience."
                )
    except Exception as e:
        print(f"⚠️ Date comparison failed: {e}", file=sys.stderr)

    return (
        f"📦 **Order #{order_id}**:\n"
        f"- Product: {description}\n"
        f"- Price: ₹{price}\n"
        f"- Completed: {'✅ Yes' if completed else '❌ No'}\n"
        f"- Refundable: {'✅ Yes' if refundable else '❌ No'}\n"
        f"- Dispatch Date: {fmt(dispatch_date)}\n"
        f"- Expected Delivery: {fmt(expected_date)}\n"
        f"- Delivery Date: {fmt(delivery_date)}"
    )
