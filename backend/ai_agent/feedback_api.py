import sys
import json
import traceback
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def process_feedback(user_id, query_id, feedback_type, feedback_text=None):
    """
    Process user feedback on AI responses
    
    Args:
        user_id (int): The user's ID
        query_id (str): The unique ID of the original query
        feedback_type (str): Type of feedback (positive/negative)
        feedback_text (str, optional): Optional detailed feedback
        
    Returns:
        dict: Status of the feedback submission
    """
    try:
        # In a real implementation, you would store this feedback in a database
        # and potentially use it for improving responses
        
        feedback_id = f"fb_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Log the feedback (in production, store in database)
        feedback_data = {
            "feedback_id": feedback_id,
            "query_id": query_id,
            "user_id": user_id,
            "feedback_type": feedback_type,
            "feedback_text": feedback_text,
            "timestamp": datetime.now().isoformat()
        }
        
        # Here you would typically save to database
        print(f"Received feedback: {feedback_data}", file=sys.stderr)
        
        return {
            "success": True,
            "feedback_id": feedback_id,
            "message": "Feedback recorded successfully"
        }
        
    except Exception as e:
        error_message = str(e)
        error_traceback = traceback.format_exc()
        
        # Log the error
        print(f"Error processing feedback: {error_message}", file=sys.stderr)
        print(error_traceback, file=sys.stderr)
        
        # Return error response
        return {
            "success": False,
            "error": "An error occurred while processing your feedback",
            "error_details": error_message
        }

if __name__ == "__main__":
    try:
        # Get input data from command line argument
        input_data = json.loads(sys.argv[1])
        
        # Extract parameters
        user_id = input_data.get('user_id')
        query_id = input_data.get('query_id')
        feedback_type = input_data.get('feedback_type')
        feedback_text = input_data.get('feedback_text')
        
        # Process the feedback
        result = process_feedback(user_id, query_id, feedback_type, feedback_text)
        
        # Return JSON response
        print(json.dumps(result))
        
    except Exception as e:
        error_response = {
            "success": False,
            "error": "Failed to process feedback",
            "error_details": str(e)
        }
        print(json.dumps(error_response))