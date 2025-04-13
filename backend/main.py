# main.py
import os
import argparse
import logging
from dotenv import load_dotenv
from services.response_service import ResponseService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Agentic AI Customer Support System')
    parser.add_argument('--pdf', type=str, help='Path to instructions PDF file')
    # parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--user-id', type=str, help='User ID for the session')  # Add this line
    parser.add_argument('--query', type=str, help='User query for direct response')

    args = parser.parse_args()
    
    try:
        # Initialize the response service
        response_service = ResponseService(instructions_pdf_path=args.pdf)
        
        # if args.interactive:
        #     run_interactive_mode(response_service)
        # else:
        #     # Default to API server mode
        #     run_api_server(response_service)
        if args.user_id and args.query:
            result = response_service.get_response(args.user_id, args.query)
            print(result["response"])
            return 0


            
    except Exception as e:
        logger.error(f"Error initializing application: {e}")
        return 1
    
    return 0

def run_interactive_mode(response_service):
    """Run the system in interactive console mode for testing"""
    print("=== Agentic AI Customer Support System (Interactive Mode) ===")
    print("Type 'exit' to quit")
    
    try:
        user_id = input("Enter user ID: ")
        
        while True:
            try:
                query = input("\nUser Query: ")
                
                if query.lower() == 'exit':
                    print("Exiting the program...")
                    break
                    
                # Generate response
                print("Generating response...")
                result = response_service.get_response(user_id, query)
                
                print("\nAI Response:")
                print(result["response"])
                
                # Get feedback
                feedback = input("\nWas this response helpful? (y/n): ")
                if feedback.lower() in ['y', 'yes']:
                    rating = int(input("Rate the response (1-5): "))
                    comments = input("Any comments? (optional): ")
                    
                    # Save feedback
                    response_service.save_feedback(
                        result["conversation_id"],
                        rating,
                        comments,
                        helpful=(feedback.lower() in ['y', 'yes'])
                    )
                    print("Feedback saved.")
                else:
                    print("Thanks for your feedback.")
                    
            except KeyboardInterrupt:
                print("\nOperation interrupted. Type 'exit' to quit or continue with a new query.")
                continue
            except Exception as e:
                print(f"\nError: {e}")
                print("Please try again.")
                continue
    
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting.")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        print("Thank you for using the AI Customer Support System.")
        
def run_api_server(response_service):
    """Run the system as a REST API server"""
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    @app.route('/api/query', methods=['POST'])
    def handle_query():
        try:
            data = request.json
            user_id = data.get('user_id')
            query = data.get('query')
            
            if not user_id or not query:
                return jsonify({"error": "Missing user_id or query"}), 400
                
            result = response_service.get_response(user_id, query)
            
            return jsonify({
                "response": result["response"],
                "conversation_id": result["conversation_id"]
            })
            
        except Exception as e:
            logger.error(f"API error: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/feedback', methods=['POST'])
    def handle_feedback():
        try:
            data = request.json
            conversation_id = data.get('conversation_id')
            rating = data.get('rating')
            comments = data.get('comments')
            helpful = data.get('helpful', True)
            
            if not conversation_id or not rating:
                return jsonify({"error": "Missing conversation_id or rating"}), 400
                
            success = response_service.save_feedback(conversation_id, rating, comments, helpful)
            
            if success:
                return jsonify({"status": "feedback saved"})
            else:
                return jsonify({"error": "Failed to save feedback"}), 500
                
        except Exception as e:
            logger.error(f"API error: {e}")
            return jsonify({"error": str(e)}), 500
    
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()