import sys
import json
import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI

# 🌱 Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 🔧 Tool function to check order status
def check_order_status(order_id: str) -> str:
    fake_orders = {
        "12345": "Order #12345 is out for delivery and should arrive by 6 PM today.",
        "67890": "Order #67890 was delivered on April 6th.",
        "77777": "Order #77777 is delayed due to weather and will arrive tomorrow."
    }
    return fake_orders.get(order_id, "Sorry, I couldn't find an order with that ID.")

# 🔨 Tool definition
check_order_status_tool = Tool(
    name="check_order_status",
    func=check_order_status,
    description="Checks order status given an order ID."
)

# 🧠 Set up LLM with Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # Correct model name
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)

# 🧠 Set up memory and agent
memory = ConversationBufferMemory()
agent = initialize_agent(
    tools=[check_order_status_tool],
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory
)

# 🔁 Subprocess support to run the agent
def run_agent(user_input: str) -> str:
    return agent.run(user_input)

# 🔄 Main entry point to process stdin input
if __name__ == "__main__":
    try:
        input_data = sys.stdin.read()  # Read the input data
        data = json.loads(input_data)  # Parse the input data
        message = data.get("message", "")  # Get the message
        result = run_agent(message)  # Run the agent with the input
        print(json.dumps({"response": result}))  # Output the result as JSON
    except Exception as e:
        print(json.dumps({"error": str(e)}))  # Handle errors and return as JSON

# testing:
# echo '{"message": "Track order 12345"}' | python3 langchain/langchain_agent.py

