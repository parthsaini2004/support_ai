# services/response_service.py
import json 
from services.ai_service import AIService
from services.context_service import ContextService
from models.conversation import ConversationModel
from models.feedback import FeedbackModel
from utils.pdf_parser import PDFInstructionsParser
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResponseService:
    def __init__(self, instructions_pdf_path=None):
        self.ai_service = AIService()
        self.context_service = ContextService()
        self.conversation_model = ConversationModel()
        self.feedback_model = FeedbackModel()
        
        # Load instructions from PDF if provided
        self.instructions = None
        if instructions_pdf_path:
            pdf_parser = PDFInstructionsParser()
            self.instructions = pdf_parser.parse(instructions_pdf_path)
    
    def get_response(self, user_id, query):
        """Generate a response for the user query"""
        try:
            # Build context
            context = self.context_service.build_context(user_id, query)
            
            # Add instructions to context if available
            if self.instructions:
                context_obj = json.loads(context)
                context_obj["instructions"] = self.instructions
                context = json.dumps(context_obj)
            
            # Generate response using AI service
            response = self.ai_service.generate_response(query, context)
            
            # Save conversation
            conversation_id = self.conversation_model.create_conversation(user_id, query, response)
            
            return {
                "response": response,
                "conversation_id": conversation_id
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "response": "I'm sorry, I encountered an error while processing your request. Please try again later.",
                "error": str(e)
            }
    
    def save_feedback(self, conversation_id, rating, comments=None, helpful=True):
        """Save feedback for a conversation"""
        try:
            # Update feedback in conversation
            self.conversation_model.update_feedback(conversation_id, {
                "rating": rating,
                "comments": comments,
                "helpful": helpful
            })
            
            # Save detailed feedback
            self.feedback_model.save_feedback(conversation_id, rating, comments, helpful)
            
            return True
        except Exception as e:
            logger.error(f"Error saving feedback: {e}")
            return False