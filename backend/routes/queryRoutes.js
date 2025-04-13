import express from 'express';
import { processQuery, submitFeedback } from '../controllers/queryController.js';
import { protect } from '../middleware/authMiddleware.js';
import User from '../models/User.js';
import Order from '../models/Order.js';
import runPythonScript from '../utils/pythonRunner.js';

const router = express.Router();

// Protected routes - require authentication
router.post('/query', protect, processQuery);
router.post('/feedback', protect, submitFeedback);

// Test endpoint that doesn't require authentication (for development only)
router.post('/query-test', async (req, res) => {
  try {
    const { message, user_id } = req.body;
    
    if (!message) {
      return res.status(400).json({ success: false, error: 'Query message is required' });
    }
    
    if (!user_id) {
      return res.status(400).json({ success: false, error: 'User ID is required for test endpoint' });
    }

    // Fetch user data to provide context to the AI
    const user = await User.findOne({ user_id });
    if (!user) {
      return res.status(404).json({ success: false, error: 'User not found' });
    }

    // Get user's orders for context
    const orders = await Order.find({ user_id });
    
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
      user_id,
      message,
      context: contextData
    });

    // Return the AI response
    return res.status(200).json({
      success: true,
      response
    });
  } catch (error) {
    console.error('Test query processing error:', error.message);
    return res.status(500).json({
      success: false,
      error: 'An error occurred while processing your test query'
    });
  }
});

export default router;