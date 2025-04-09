import sys
import os
import json

# Add the project root (parent of 'backend') to sys.path so that absolute imports work.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.langchain.classifier import classify_request
from backend.langchain.order_tools import order_tool_wrapper, tool_function_with_user
from backend.langchain.db_utils import GOOGLE_API_KEY

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI

# 🧠 Set up LLM with Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)

# 🔁 Main function to process input
def run_agent(user_input: str, user_id: int) -> str:
    try:
        request_type = str(classify_request(user_input)).strip().lower()
    except Exception as e:
        print(f"⚠️ classify_request failed: {e}", file=sys.stderr)
        return "❗ I couldn't understand your request at the moment."

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

    elif request_type == "greeting":
        return "👋 Hello! How can I assist you today?"

    else:
        return "❗ I am not made to handle such requests."


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
