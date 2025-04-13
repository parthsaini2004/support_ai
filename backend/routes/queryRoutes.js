// routes/queryRoutes.js
import express from 'express';
import { handleQuery } from '../controllers/queryController.js';
import { protect as authenticateUser } from '../middleware/authMiddleware.js';


const router = express.Router();

// POST /api/query
router.post('/query', authenticateUser, handleQuery);

export default router;
