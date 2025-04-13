# services/ai_service.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in the environment variables")
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # System instructions for the model
        self.system_instructions = """
        You are an AI customer support agent. Your goal is to assist users with their queries
        about orders, refunds, and account information. Use the provided context to give accurate
        and helpful responses. Be friendly, concise, and always try to resolve the customer's issue.
        If you don't know the answer, acknowledge that and offer to escalate the issue to a human agent.
        """
    
    def generate_response(self, prompt, context=None):
        """Generate a response using the Gemini model"""
        try:
            # Build the complete prompt with context
            complete_prompt = self._build_prompt(prompt, context)
            
            # Generate response
            response = self.model.generate_content(
                complete_prompt,
                generation_config={
                    "temperature": 0.2,
                    "top_p": 0.9,
                    "top_k": 40,
                    "max_output_tokens": 1024,
                }
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return "I'm sorry, I encountered an error while processing your request. Please try again later."
    
    def _build_prompt(self, user_query, context=None):
        """Build the complete prompt with context"""
        if context:
            complete_prompt = f"{self.system_instructions}\n\nContext Information:\n{context}\n\nUser Query: {user_query}\n\nResponse:"
        else:
            complete_prompt = f"{self.system_instructions}\n\nUser Query: {user_query}\n\nResponse:"
        
        return complete_prompt