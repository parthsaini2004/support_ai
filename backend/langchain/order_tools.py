import sys
from .db_utils import fetch_order_info
from langchain.agents import Tool

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
