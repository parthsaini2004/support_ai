import sys
import json
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv
import traceback

# Import services
from services.ai_service import get_ai_response
from services.context_service import build_context
from services.response_service import format_response

# Load environment variables
load_dotenv()

def process_query(user_id, message, context):
    """
    Process a user query with AI assistance
    
    Args:
        user_id (int): The user's ID
        message (str): The user's query text
        context (dict): User and order context data
        
    Returns:
        dict: The AI response with metadata
    """
    try:
        # Generate a unique query ID
        query_id = str(uuid.uuid4())
        
        # Build context from user data and orders
        context_text = build_context(context)
        
        # Get AI response
        ai_response = get_ai_response(message, context_text)
        
        # Format the final response
        formatted_response = format_response(ai_response)
        
        # Return the response with metadata
        response = {
            "query_id": query_id,
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "response": formatted_response,
            "success": True
        }
        
        return response
        
    except Exception as e:
        error_message = str(e)
        error_traceback = traceback.format_exc()
        
        # Log the error
        print(f"Error processing query: {error_message}", file=sys.stderr)
        print(error_traceback, file=sys.stderr)
        
        # Return error response
        return {
            "success": False,
            "error": "An error occurred while processing your query",
            "error_details": error_message
        }

if __name__ == "__main__":
    try:
        # Get input data from command line argument
        input_data = json.loads(sys.argv[1])
        
        # Extract parameters
        user_id = input_data.get('user_id')
        message = input_data.get('message')
        context = input_data.get('context', {})
        
        # Process the query
        result = process_query(user_id, message, context)
        
        # Return JSON response
        print(json.dumps(result))
        
    except Exception as e:
        error_response = {
            "success": False,
            "error": "Failed to process input",
            "error_details": str(e)
        }
        print(json.dumps(error_response))