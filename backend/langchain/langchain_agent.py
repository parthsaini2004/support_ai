# backend/langchain/langchain_agent.pyimport import sys
import json
import sys 
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from pymongo import MongoClient

from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI

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

# 🧰 Wrapper for LangChain Tool
def order_tool_wrapper(query: str, default_user_id: int) -> str:
    try:
        parts = query.strip().split()
        if len(parts) < 1:
            return "❗ Please provide a valid Order ID."
        
        order_id = int(parts[0])
        user_id = default_user_id

        if len(parts) >= 2:
            user_id = int(parts[1])

        return fetch_order_info(order_id, user_id)
    except Exception as e:
        return f"⚠️ Error parsing input: {str(e)}"

# 🔨 Tool definition
def tool_function_with_user(user_id: int):
    return Tool(
        name="check_order_status",
        func=lambda query: order_tool_wrapper(query, user_id),
        description="Use this to check order status. Input format: '<order_id>' or '<order_id> <user_id>'"
    )

# 🧠 Set up LLM with Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)

# 🧠 Classify the type of request
def classify_request(message: str) -> str:
    message_lower = message.lower()

    delivery_keywords = ["order", "delivery", "not received", "delayed", "shipped", "dispatch"]
    account_keywords = ["password", "account", "login", "reset", "sign in", "authentication"]

    if any(word in message_lower for word in delivery_keywords):
        return "delivery_query"
    elif any(word in message_lower for word in account_keywords):
        return "user_account"
    else:
        return "general"

# 🔁 Main function to process input
def run_agent(user_input: str, user_id: int) -> str:
    request_type = classify_request(user_input)

    if request_type == "delivery_query":
        import re
        match = re.findall(r'\d+', user_input)
        if len(match) >= 1:
            order_id = int(match[0])
            return order_tool_wrapper(str(order_id), user_id)
        else:
            return (
                "❗ It seems like you're asking about an order or delivery, "
                "but I need the Order ID to help. "
                "Example: 'My order 5001 is delayed.'"
            )

    elif request_type == "user_account":
        return (
            "🔐 This looks like an account-related issue. "
            "To reset your password, please go to your account settings. "
            "If you're still having trouble, our support team can help further."
        )

    memory = ConversationBufferMemory()
    agent = initialize_agent(
        tools=[tool_function_with_user(user_id)],
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory
    )
    return agent.run(user_input)

# 🚀 Entrypoint
if __name__ == "__main__":
    try:
        input_data = sys.stdin.read()
        print(f"📨 Received input: {input_data}", file=sys.stderr)

        data = json.loads(input_data)
        message = data.get("message", "")
        user_id = int(data.get("user_id", 0))

        result = str(run_agent(message, user_id))
        print(json.dumps({"response": result}), flush=True)

    except Exception as e:
        print(f"💥 Exception occurred: {str(e)}", file=sys.stderr)
        print(json.dumps({"error": str(e)}), flush=True)
