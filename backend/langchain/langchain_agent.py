# backend/langchain/langchain_agent.py
import sys
import json
import os
from datetime import datetime
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

# ✅ Make sure this is EXACTLY the DB name you use in Atlas
db = client["orderAi"]  # <-- Replace this with the real DB name
orders_collection = db["orders"]

# 📦 Fetch order info by order_id and user_id
def fetch_order_info(order_id: int, user_id: int) -> str:
    # 🔍 Debug print
    print(f"📂 Using DB: {db.name}, Collection: {orders_collection.name}", file=sys.stderr)
    print(f"🔢 Total Orders: {orders_collection.count_documents({})}", file=sys.stderr)

    # 🔎 Find order
    order = orders_collection.find_one({
        "order_id": int(order_id),
        "user_id": int(user_id)
    })

    # Debug: Print the found order
    print(f"🧾 Fetched Order: {order}", file=sys.stderr)

    if not order:
        return f"❌ No order found with ID {order_id} for user {user_id}."

    status = order.get("status", {})
    delivery_date = status.get("delivery_date")
    expected_date = status.get("expected_delivery_date")
    dispatch_date = status.get("dispatch_date")

    description = order.get("description", "No description available")
    price = order.get("price", "N/A")
    completed = order.get("completed", False)
    refundable = order.get("refund", {}).get("refundable", False)

    def fmt(date_val):
        if isinstance(date_val, str):
            date_val = datetime.fromisoformat(date_val.replace("Z", "+00:00"))
        return date_val.strftime("%B %d, %Y") if date_val else "Not available"

    return (
        f"📦 **Order #{order_id}** for user {user_id}:\n"
        f"- Product: {description}\n"
        f"- Price: ₹{price}\n"
        f"- Completed: {'✅ Yes' if completed else '❌ No'}\n"
        f"- Refundable: {'✅ Yes' if refundable else '❌ No'}\n"
        f"- Dispatch Date: {fmt(dispatch_date)}\n"
        f"- Expected Delivery: {fmt(expected_date)}\n"
        f"- Delivery Date: {fmt(delivery_date)}"
    )

# 🧰 Wrapper for LangChain Tool
def order_tool_wrapper(query: str) -> str:
    try:
        parts = query.strip().split()
        if len(parts) < 2:
            return "❗ Please provide both order ID and user ID. Example: '5001 101'"
        order_id = int(parts[0])
        user_id = int(parts[1])
        return fetch_order_info(order_id, user_id)
    except Exception as e:
        return f"⚠️ Error parsing input: {str(e)}"

# 🔨 Tool definition
check_order_status_tool = Tool(
    name="check_order_status",
    func=order_tool_wrapper,
    description="Use this to check order status. Input format: '<order_id> <user_id>'"
)

# 🧠 Set up LLM with Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)

# 🧠 Memory and agent setup
memory = ConversationBufferMemory()
agent = initialize_agent(
    tools=[check_order_status_tool],
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory
)

# 🔁 Main function to process input via stdin
def run_agent(user_input: str) -> str:
    return agent.run(user_input)

if __name__ == "__main__":
    try:
        input_data = sys.stdin.read()
        data = json.loads(input_data)
        message = data.get("message", "")
        result = run_agent(message)
        print(json.dumps({"response": result}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))