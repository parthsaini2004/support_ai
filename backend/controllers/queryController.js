// controllers/queryController.js
import { pythonRunner } from '../utils/pythonRunner.js';

export const handleQuery = async (req, res) => {
  try {
    const userId = req.user.user_id;
    const { query } = req.body;

    if (!query) {
      return res.status(400).json({ error: 'Query is required' });
    }

    const result = await pythonRunner(userId, query);
    res.status(200).json({ response: result });
  } catch (error) {
    console.error('Query handling failed:', error);
    res.status(500).json({ error: 'Failed to process query' });
  }
};
