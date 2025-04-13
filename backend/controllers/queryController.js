import runPythonScript from '../utils/pythonRunner.js';
import User from '../models/User.js';
import Order from '../models/Order.js';

export const processQuery = async (req, res) => {
  try {
    const { message } = req.body;
    
    // Check if user is properly authenticated
    if (!req.user || !req.user.user_id) {
      return res.status(401).json({ 
        success: false, 
        error: 'Authentication required. User information not found.' 
      });
    }
    
    const userId = req.user.user_id;
    
    if (!message) {
      return res.status(400).json({ success: false, error: 'Query message is required' });
    }

    // Fetch user data to provide context to the AI
    const user = await User.findOne({ user_id: userId });
    if (!user) {
      return res.status(404).json({ success: false, error: 'User not found' });
    }

    // Get user's orders for context
    const orders = await Order.find({ user_id: userId });
    
    // Prepare contextual data for the AI agent
    const contextData = {
      user: {
        user_id: user.user_id,
        username: user.username,
        email: user.email,
        id_creation_date: user.id_creation_date
      },
      orders: orders.map(order => ({
        order_id: order.order_id,
        completed: order.completed,
        status: {
          expected_delivery_date: order.status.expected_delivery_date,
          delivery_date: order.status.delivery_date,
          dispatch_date: order.status.dispatch_date
        },
        order_date: order.order_date,
        price: order.price,
        description: order.description,
        refund: {
          refundable: order.refund.refundable,
          refundable_within: order.refund.refundable_within
        }
      }))
    };

    // Pass the query and context to the Python AI agent
    const response = await runPythonScript('ai_agent/agent_api.py', {
      user_id: userId,
      message: message,
      context: contextData
    });

    // Return the AI response
    return res.status(200).json({
      success: true,
      response
    });
  } catch (error) {
    console.error('Query processing error:', error.message);
    return res.status(500).json({
      success: false,
      error: 'An error occurred while processing your query'
    });
  }
};

export const submitFeedback = async (req, res) => {
  try {
    // Check if user is properly authenticated
    if (!req.user || !req.user.user_id) {
      return res.status(401).json({ 
        success: false, 
        error: 'Authentication required. User information not found.' 
      });
    }
    
    const userId = req.user.user_id;
    const { query_id, feedback_type, feedback_text } = req.body;
    
    if (!query_id || !feedback_type) {
      return res.status(400).json({ success: false, error: 'Query ID and feedback type are required' });
    }

    // Pass the feedback to the Python feedback API
    const result = await runPythonScript('ai_agent/feedback_api.py', {
      user_id: userId,
      query_id,
      feedback_type,
      feedback_text
    });

    return res.status(200).json({
      success: true,
      message: 'Feedback submitted successfully',
      result
    });
  } catch (error) {
    console.error('Feedback submission error:', error.message);
    return res.status(500).json({
      success: false,
      error: 'An error occurred while submitting feedback'
    });
  }
};