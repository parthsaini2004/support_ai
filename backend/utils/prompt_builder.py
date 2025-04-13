# utils/prompt_builder.py
import json

class PromptBuilder:
    def __init__(self):
        pass
    
    def build_customer_support_prompt(self, query, context, instructions=None):
        """
        Build a structured prompt for the AI model with user context and query
        """
        # Parse context if it's a string
        if isinstance(context, str):
            try:
                context = json.loads(context)
            except:
                context = {"error": "Invalid context format"}
        
        # Start with system instructions
        prompt = "You are an AI customer support agent helping a user with their query.\n\n"
        
        # Add user details
        user = context.get("user", {})
        if user and user.get("user_id"):
            prompt += f"User Information:\n"
            prompt += f"- User ID: {user.get('user_id')}\n"
            prompt += f"- Username: {user.get('username')}\n"
            prompt += f"- Account created: {user.get('id_creation_date')}\n\n"
        
        # Add conversation history
        history = context.get("conversation_history", [])
        if history:
            prompt += "Recent Conversation History:\n"
            for i, conv in enumerate(history, 1):
                prompt += f"Conversation {i}:\n"
                prompt += f"- User: {conv.get('query')}\n"
                prompt += f"- Agent: {conv.get('response')}\n"
            prompt += "\n"
        
        # Add order information
        orders = context.get("orders", [])
        if orders:
            prompt += "Order Information:\n"
            for order in orders:
                prompt += f"- Order #{order.get('order_id')}: {order.get('description')}\n"
                prompt += f"  Status: {'Completed' if order.get('completed') else 'In Progress'}\n"
                prompt += f"  Order Date: {order.get('order_date')}\n"
                prompt += f"  Price: ${order.get('price')}\n"
                
                # Add delivery information
                status = order.get("status", {})
                if status:
                    if status.get("dispatch_date"):
                        prompt += f"  Dispatched: {status.get('dispatch_date')}\n"
                    if status.get("expected_delivery_date"):
                        prompt += f"  Expected Delivery: {status.get('expected_delivery_date')}\n"
                    if status.get("delivery_date"):
                        prompt += f"  Delivered: {status.get('delivery_date')}\n"
                
                # Add refund information
                refund = order.get("refund", {})
                if refund:
                    refundable = refund.get("refundable", False)
                    prompt += f"  Refundable: {'Yes' if refundable else 'No'}\n"
                    if refundable and refund.get("refundable_within"):
                        prompt += f"  Refundable Until: {refund.get('refundable_within')}\n"
                
                prompt += "\n"
        
        # Add custom instructions if available
        if instructions:
            prompt += "Special Instructions:\n"
            for category, inst_list in instructions.items():
                if inst_list:
                    prompt += f"{category.title()}:\n"
                    for inst in inst_list:
                        prompt += f"- {inst}\n"
            prompt += "\n"
        
        # Add the current query
        prompt += f"Current User Query: {query}\n\n"
        
        # Add response instructions
        prompt += "Please provide a helpful, accurate, and concise response to the user query based on the information provided above. If you don't have enough information to answer fully, acknowledge what you know and what you don't. Maintain a friendly and professional tone."
        
        return prompt