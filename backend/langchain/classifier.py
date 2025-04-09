import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Gemini 2.0 Flash LLM setup
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)

# List of valid categories
VALID_CATEGORIES = ["greeting", "delivery_query", "user_account", "general","ending"]

def classify_request(message: str) -> str:
    prompt = f"""
You are an intent classifier. Based on the message below, classify it into **one** of the following categories:
- greeting
- delivery_query
- user_account
- general

Respond with ONLY the category name (no punctuation, no explanation).

Examples:
User: "Hi there, how are you?" → greeting  
User: "bye bye " → ending  
User: "Where is my order 129?" → delivery_query  
User: "I want to delete my account" → user_account  
User: "Tell me more about your products" → general  

Now classify this message:
"{message}"
"""
    try:
        response = llm.invoke([HumanMessage(content=prompt)]).content.strip().lower()
        # ✅ Log to stderr so it doesn't interfere with JSON output
        print(f"[Gemini Classification]: {response}", file=sys.stderr)
        return response if response in VALID_CATEGORIES else "general"
    except Exception as e:
        print(f"[Classifier Error]: {e}", file=sys.stderr)
        return "general"
