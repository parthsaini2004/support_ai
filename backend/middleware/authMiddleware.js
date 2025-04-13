import jwt from 'jsonwebtoken';
import User from '../models/User.js';

/**
 * Middleware to protect routes requiring authentication
 * Verifies JWT token and attaches user to request object
 */
export const protect = async (req, res, next) => {
  let token;

  // Check for token in Authorization header
  if (
    req.headers.authorization &&
    req.headers.authorization.startsWith('Bearer')
  ) {
    try {
      // Extract token from header
      token = req.headers.authorization.split(' ')[1];

      // Verify token
      const decoded = jwt.verify(token, process.env.JWT_SECRET);

      // Find user and attach to request (exclude password)
      req.user = await User.findOne({ user_id: decoded.userId }).select('-password');

      next();
    } catch (error) {
      console.error('Authentication error:', error.message);
      res.status(401).json({ 
        success: false, 
        error: 'Not authorized, token failed' 
      });
    }
  }

  // Check for token in cookies as fallback
  else if (req.cookies && req.cookies.token) {
    try {
      token = req.cookies.token;
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      req.user = await User.findOne({ user_id: decoded.userId }).select('-password');
      next();
    } catch (error) {
      console.error('Cookie authentication error:', error.message);
      res.status(401).json({ 
        success: false, 
        error: 'Not authorized, token failed' 
      });
    }
  }

  if (!token) {
    res.status(401).json({ 
      success: false, 
      error: 'Not authorized, no token provided' 
    });
  }
};

/**
 * Middleware to check if user is an admin
 * Must be used after the protect middleware
 */
export const admin = (req, res, next) => {
  if (req.user && req.user.isAdmin) {
    next();
  } else {
    res.status(403).json({ 
      success: false, 
      error: 'Not authorized as an admin' 
    });
  }
};